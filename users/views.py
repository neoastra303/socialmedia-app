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
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from posts.models import Post
from notifications.utils import send_notification

# Create your views here.

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
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
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    if request.method == 'POST' and user == request.user:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('تم تحديث ملفك الشخصي بنجاح!'))
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {
        'user': user,
        'posts': posts,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('تم تسجيل خروجك بنجاح!'))
    return redirect('users:login')

@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    return render(request, 'users/login.html')

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
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
    return redirect('users:profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.profile.unfollow(user_to_unfollow)
    messages.success(request, _(f'أنت لم تعد تتابع {username}'))
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
