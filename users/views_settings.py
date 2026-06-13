from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@login_required
def settings_view(request):
    return render(request, 'users/settings.html', {
        'password_form': PasswordChangeForm(user=request.user),
    })

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/settings.html'
    success_url = reverse_lazy('users:settings')

    def form_valid(self, form):
        messages.success(self.request, _('تم تغيير كلمة المرور بنجاح.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('خطأ في تغيير كلمة المرور.'))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = context.get('form', PasswordChangeForm(user=self.request.user))
        context['active_tab'] = 'password'
        return context

@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        if not request.user.check_password(password):
            messages.error(request, _('كلمة المرور غير صحيحة.'))
            return redirect('users:settings')
        if not new_email:
            messages.error(request, _('البريد الإلكتروني مطلوب.'))
            return redirect('users:settings')
        if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
            messages.error(request, _('البريد الإلكتروني مستخدم بالفعل.'))
            return redirect('users:settings')
        request.user.email = new_email
        request.user.save()
        messages.success(request, _('تم تغيير البريد الإلكتروني بنجاح.'))
        return redirect('users:settings')
    return redirect('users:settings')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')
        if confirm != 'DELETE':
            messages.error(request, _('يرجى كتابة DELETE لتأكيد الحذف.'))
            return redirect('users:settings')
        if not request.user.check_password(password):
            messages.error(request, _('كلمة المرور غير صحيحة.'))
            return redirect('users:settings')
        user = request.user
        user.delete()
        messages.success(request, _('تم حذف الحساب بنجاح.'))
        return redirect('users:register')
    return redirect('users:settings')
