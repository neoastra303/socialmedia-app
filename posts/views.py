from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from middleware.rate_limiting import post_creation_ratelimit, user_ratelimit
from django.core.exceptions import ValidationError
from .models import Post, Comment, Hashtag, Reaction, Story
from notifications.utils import send_notification
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@login_required
def post_list(request):
    blocked = request.user.profile.blocked_users.values_list('user_id', flat=True)
    blocked_by = request.user.profile.blocked_by.values_list('user_id', flat=True)
    exclude_ids = set(blocked) | set(blocked_by)
    posts = Post.objects.select_related('author').exclude(author_id__in=exclude_ids).order_by('-created_at')
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'posts/post_list.html', {'page_obj': page_obj})

@login_required
def post_detail(request, post_id):
    """عرض تفاصيل منشور معين"""
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)
    comments = post.comments.select_related('author').all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, _('تم إضافة تعليقك بنجاح!'))
                # Send notification
                if request.user != post.author:
                    send_notification(
                        post.author,
                        f'{request.user.username} علق على منشورك',
                        'comment',
                        related_user=request.user,
                        related_post=post
                    )
                return redirect('posts:post_detail', post_id=post.id)
            except ValidationError as e:
                messages.error(request, _('خطأ في التحقق من التعليق: ') + str(e))
            except Exception as e:
                logger.error(f"Error saving comment: {str(e)}")
                messages.error(request, _('حدث خطأ أثناء حفظ التعليق.'))
        else:
            # Handle form errors
            for field, errors in comment_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        comment_form = CommentForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
@post_creation_ratelimit
def post_create(request):
    """إنشاء منشور جديد"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, _('تم إنشاء المنشور بنجاح!'))
                return redirect('posts:post_list')
            except ValidationError as e:
                messages.error(request, _('خطأ في التحقق من المنشور: ') + str(e))
            except Exception as e:
                logger.error(f"Error creating post: {str(e)}")
                messages.error(request, _('حدث خطأ أثناء إنشاء المنشور.'))
        else:
            # Handle form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})

@login_required
@ratelimit(key='user', rate='5/m', method='POST', block=True)
def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)

    if post.author != request.user:
        messages.error(request, _('لا يمكنك تعديل منشور شخص آخر.'))
        return redirect('posts:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('تم تحديث المنشور بنجاح!'))
                return redirect('posts:post_detail', post_id=post.id)
            except ValidationError as e:
                messages.error(request, _('خطأ في التحقق من المنشور: ') + str(e))
            except Exception as e:
                logger.error(f"Error updating post: {str(e)}")
                messages.error(request, _('حدث خطأ أثناء تحديث المنشور.'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})

@login_required
@ratelimit(key='user', rate='5/m', method='POST', block=True)
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, _('تم حذف المنشور بنجاح!'))
        return redirect('posts:post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def react_to_post(request, post_id):
    try:
        post = get_object_or_404(Post.objects.select_related('author'), id=post_id)
        reaction_type = request.POST.get('reaction', 'like')

        valid_reactions = [choice[0] for choice in Reaction.REACTION_CHOICES]
        if reaction_type not in valid_reactions:
            return JsonResponse({
                'status': 'error',
                'message': _('نوع التفاعل غير صالح.')
            }, status=400)

        reaction, created = Reaction.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )

        if not created:
            if reaction.reaction_type == reaction_type:
                reaction.delete()
                reacted = False
                reaction_type = None
            else:
                reaction.reaction_type = reaction_type
                reaction.save()
                reacted = True
                if request.user != post.author:
                    send_notification(
                        post.author,
                        f'{request.user.username} تفاعل على منشورك بـ {reaction_type}',
                        'reaction',
                        related_user=request.user,
                        related_post=post
                    )
        else:
            reacted = True
            if request.user != post.author:
                send_notification(
                    post.author,
                    f'{request.user.username} تفاعل على منشورك بـ {reaction_type}',
                    'reaction',
                    related_user=request.user,
                    related_post=post
                )

        return JsonResponse({
            'status': 'success',
            'reacted': reacted,
            'reaction_type': reaction_type,
            'total_reactions': post.total_reactions()
        })
    except Exception as e:
        logger.error(f"Error processing reaction: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': _('حدث خطأ أثناء معالجة التفاعل.')
        }, status=500)

@login_required
def hashtag_posts(request, hashtag_name):
    """عرض المنشورات حسب الهاشتاج"""
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    posts = hashtag.posts.select_related('author').all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/hashtag_posts.html', {'hashtag': hashtag, 'page_obj': page_obj})

@login_required
def search(request):
    """البحث المتقدم في المنشورات والمستخدمين"""
    try:
        query = request.GET.get('q', '')
        filter_type = request.GET.get('type', 'all')  # all, posts, users

        results = {
            'posts': [],
            'users': [],
            'query': query,
            'filter_type': filter_type
        }

        # Validate filter type
        valid_filter_types = ['all', 'posts', 'users']
        if filter_type not in valid_filter_types:
            filter_type = 'all'

        if query:
            if filter_type in ['all', 'posts']:
                blocked = request.user.profile.blocked_users.values_list('user_id', flat=True)
                blocked_by = request.user.profile.blocked_by.values_list('user_id', flat=True)
                posts = Post.objects.filter(
                    Q(content__icontains=query) |
                    Q(hashtags__name__icontains=query)
                ).exclude(author_id__in=set(blocked) | set(blocked_by)
                ).select_related('author').distinct().order_by('-created_at')
                paginator = Paginator(posts, 10)
                page_number = request.GET.get('page')
                results['posts'] = paginator.get_page(page_number)

            if filter_type in ['all', 'users']:
                # Search in users
                blocked = request.user.profile.blocked_users.values_list('user_id', flat=True)
                blocked_by = request.user.profile.blocked_by.values_list('user_id', flat=True)
                users = User.objects.filter(
                    Q(username__icontains=query) |
                    Q(profile__bio__icontains=query)
                ).exclude(id__in=set(blocked) | set(blocked_by)).distinct()
                results['users'] = users

        return render(request, 'posts/search_results.html', results)
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        messages.error(request, _('حدث خطأ أثناء البحث.'))
        return render(request, 'posts/search_results.html', {
            'posts': [],
            'users': [],
            'query': '',
            'filter_type': 'all'
        })

@login_required
def stories_list(request):
    """عرض القصص النشطة"""
    stories = Story.objects.select_related('author').filter(expires_at__gt=timezone.now()).order_by('-created_at')
    return render(request, 'posts/stories_list.html', {'stories': stories})

@login_required
def create_story(request):
    """إنشاء قصة جديدة"""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        # Validate that only one of image or video is provided
        if image and video:
            messages.error(request, _('لا يمكن إنشاء قصة تحتوي على صورة وفيديو في نفس الوقت.'))
            return render(request, 'posts/create_story.html')
        
        try:
            story = Story(
                author=request.user,
                content=content,
                image=image,
                video=video
            )
            story.full_clean()  # This will run model validation
            story.save()
            messages.success(request, _('تم إنشاء القصة بنجاح!'))
            return redirect('posts:stories_list')
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            else:
                messages.error(request, _('خطأ في التحقق من القصة: ') + str(e))
        except Exception as e:
            logger.error(f"Error creating story: {str(e)}")
            messages.error(request, _('حدث خطأ أثناء إنشاء القصة.'))
    
    return render(request, 'posts/create_story.html')

@login_required
def view_story(request, story_id):
    """عرض قصة معينة"""
    story = get_object_or_404(Story.objects.select_related('author'), id=story_id)
    if not story.is_expired():
        story.views.add(request.user)
    return render(request, 'posts/view_story.html', {'story': story})

@api_view(['GET'])
def api_post_list(request):
    posts = Post.objects.select_related('author').all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
