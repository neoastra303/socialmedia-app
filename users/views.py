from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django_ratelimit.decorators import ratelimit
from middleware.rate_limiting import ip_ratelimit
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from posts.models import Post
from notifications.utils import send_notification
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@ip_ratelimit
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Deactivate account until email verification
                user.save()
                # Send verification email
                current_site = get_current_site(request)
                subject = _('تفعيل حسابك في منصتي')
                message = render_to_string('users/email_verification.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(subject, message, 'noreply@mansati.com', [user.email])
                messages.success(request, _('تم إنشاء حسابك! يرجى التحقق من بريدك الإلكتروني لتفعيل الحساب.'))
                return redirect('users:login')
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                messages.error(request, _('حدث خطأ أثناء إنشاء الحساب.'))
        else:
            # Handle form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.profile.email_verified = True
        user.save()
        messages.success(request, _('تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.'))
        return redirect('users:login')
    else:
        messages.error(request, _('رابط التفعيل غير صالح.'))
        return redirect('users:register')

@login_required
def profile(request, username=None):
    try:
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user

        if request.method == 'POST' and user == request.user:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if u_form.is_valid() and p_form.is_valid():
                try:
                    u_form.save()
                    p_form.save()
                    messages.success(request, _('تم تحديث ملفك الشخصي بنجاح!'))
                    return redirect('users:profile')
                except Exception as e:
                    logger.error(f"Error updating profile: {str(e)}")
                    messages.error(request, _('حدث خطأ أثناء تحديث الملف الشخصي.'))
            else:
                for form_name, form in [('User', u_form), ('Profile', p_form)]:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{form_name} - {field}: {error}")
        else:
            u_form = UserUpdateForm(instance=user) if user == request.user else None
            p_form = ProfileUpdateForm(instance=user.profile) if user == request.user else None

        posts = Post.objects.select_related('author').filter(author=user).order_by('-created_at')
        context = {
            'user': user,
            'posts': posts,
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context)
    except Exception as e:
        logger.error(f"Error in profile view: {str(e)}")
        messages.error(request, _('حدث خطأ أثناء عرض الملف الشخصي.'))
        return redirect('posts:post_list')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('تم تسجيل خروجك بنجاح!'))
    return redirect('users:login')

@ip_ratelimit
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate input
        if not username or not password:
            messages.error(request, _('يجب إدخال اسم المستخدم وكلمة المرور.'))
            return render(request, 'users/login.html')
        
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active and user.profile.email_verified:
                    login(request, user)
                    messages.success(request, _('تم تسجيل دخولك بنجاح!'))
                    return redirect('posts:post_list')
                else:
                    messages.error(request, _('يجب تفعيل حسابك عبر البريد الإلكتروني قبل تسجيل الدخول.'))
            else:
                messages.error(request, _('اسم المستخدم أو كلمة المرور غير صحيحة'))
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            messages.error(request, _('حدث خطأ أثناء تسجيل الدخول.'))
    return render(request, 'users/login.html')

@login_required
def follow_user(request, username):
    try:
        user_to_follow = get_object_or_404(User, username=username)
        
        if request.user == user_to_follow:
            messages.warning(request, _('لا يمكنك متابعة نفسك'))
            return redirect('users:profile', username=username)
        
        if request.user.profile.following.filter(pk=user_to_follow.pk).exists():
            messages.warning(request, _(f'أنت تتابع {username} بالفعل'))
            return redirect('users:profile', username=username)
        
        if request.user.profile.follow(user_to_follow):
            messages.success(request, _(f'أنت الآن تتابع {username}'))
            # Send notification
            if request.user != user_to_follow:
                send_notification(
                    user_to_follow,
                    f'{request.user.username} بدأ يتابعك',
                    'follow',
                    related_user=request.user
                )
        else:
            messages.warning(request, _('لا يمكنك متابعة نفسك'))
    except Exception as e:
        logger.error(f"Error in follow user: {str(e)}")
        messages.error(request, _('حدث خطأ أثناء محاولة المتابعة.'))
    return redirect('users:profile', username=username)

@login_required
def unfollow_user(request, username):
    try:
        user_to_unfollow = get_object_or_404(User, username=username)
        
        if request.user == user_to_unfollow:
            messages.warning(request, _('لا يمكنك إلغاء متابعة نفسك'))
            return redirect('users:profile', username=username)
        
        if not request.user.profile.following.filter(pk=user_to_unfollow.pk).exists():
            messages.warning(request, _(f'أنت لا تتابع {username}'))
            return redirect('users:profile', username=username)
        
        request.user.profile.unfollow(user_to_unfollow)
        messages.success(request, _(f'أنت لم تعد تتابع {username}'))
    except Exception as e:
        logger.error(f"Error in unfollow user: {str(e)}")
        messages.error(request, _('حدث خطأ أثناء محاولة إلغاء المتابعة.'))
    return redirect('users:profile', username=username)

@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followers.all()
    return render(request, 'users/followers_list.html', {
        'user': user,
        'followers': followers
    })

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = user.profile.following.all()
    return render(request, 'users/following_list.html', {
        'user': user,
        'following': following
    })
