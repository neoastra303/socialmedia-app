from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from .models import Post, Comment, Hashtag, Reaction, Story
from notifications.utils import send_notification
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer

# Create your views here.

@login_required
def post_list(request):
    """عرض قائمة المنشورات"""
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'posts/post_list.html', {'page_obj': page_obj})

@login_required
def post_detail(request, post_id):
    """عرض تفاصيل منشور معين"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
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
    else:
        comment_form = CommentForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
@ratelimit(key='user', rate='5/m', method='POST', block=True)
def post_create(request):
    """إنشاء منشور جديد"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, _('تم إنشاء المنشور بنجاح!'))
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})

@login_required
def post_edit(request, post_id):
    """تعديل منشور"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث المنشور بنجاح!'))
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, post_id):
    """حذف منشور"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, _('تم حذف المنشور بنجاح!'))
        return redirect('posts:post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def react_to_post(request, post_id):
    """إضافة/تغيير/إزالة تفاعل على المنشور"""
    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.POST.get('reaction', 'like')

    reaction, created = Reaction.objects.get_or_create(
        post=post,
        user=request.user,
        defaults={'reaction_type': reaction_type}
    )

    if not created:
        if reaction.reaction_type == reaction_type:
            # Same reaction, remove it
            reaction.delete()
            reacted = False
            reaction_type = None
        else:
            # Different reaction, update it
            reaction.reaction_type = reaction_type
            reaction.save()
            reacted = True
            # Send notification if changing reaction
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
        # Send notification for new reaction
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

@login_required
def hashtag_posts(request, hashtag_name):
    """عرض المنشورات حسب الهاشتاج"""
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    posts = hashtag.posts.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/hashtag_posts.html', {'hashtag': hashtag, 'page_obj': page_obj})

@login_required
def search(request):
    """البحث المتقدم في المنشورات والمستخدمين"""
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', 'all')  # all, posts, users

    results = {
        'posts': [],
        'users': [],
        'query': query,
        'filter_type': filter_type
    }

    if query:
        if filter_type in ['all', 'posts']:
            # Search in posts content and hashtags
            posts = Post.objects.filter(
                models.Q(content__icontains=query) |
                models.Q(hashtags__name__icontains=query)
            ).distinct().order_by('-created_at')
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            results['posts'] = paginator.get_page(page_number)

        if filter_type in ['all', 'users']:
            # Search in users
            users = User.objects.filter(
                models.Q(username__icontains=query) |
                models.Q(profile__bio__icontains=query)
            ).distinct()
            results['users'] = users

    return render(request, 'posts/search_results.html', results)

@login_required
def stories_list(request):
    """عرض القصص النشطة"""
    stories = Story.objects.filter(expires_at__gt=timezone.now()).order_by('-created_at')
    return render(request, 'posts/stories_list.html', {'stories': stories})

@login_required
def create_story(request):
    """إنشاء قصة جديدة"""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        story = Story.objects.create(
            author=request.user,
            content=content,
            image=image,
            video=video
        )
        messages.success(request, _('تم إنشاء القصة بنجاح!'))
        return redirect('posts:stories_list')

    return render(request, 'posts/create_story.html')

@login_required
def view_story(request, story_id):
    """عرض قصة معينة"""
    story = get_object_or_404(Story, id=story_id)
    if not story.is_expired():
        story.views.add(request.user)
    return render(request, 'posts/view_story.html', {'story': story})

@api_view(['GET'])
def api_post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
