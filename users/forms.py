from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('اسم المستخدم'),
                'maxlength': 150
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('البريد الإلكتروني'),
                'maxlength': 254
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('كلمة المرور')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('تأكيد كلمة المرور')
        })
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError(_('A user with that username already exists.'))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            existing = User.objects.filter(email__iexact=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError(_('A user with that email already exists.'))
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 150
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'maxlength': 254
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.instance and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_('A user with that email already exists.'))
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('اكتب نبذة عنك...'),
                'maxlength': 500
            })
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB max)
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError(_('Profile image too large. Size should not exceed 5MB.'))
            
            # Check file type
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            extension = '.' + image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError(_('Invalid file format. Valid formats are: .jpg, .jpeg, .png, .gif.'))
        return image
    
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 500:
            raise ValidationError(_('Bio cannot exceed 500 characters.'))
        return bio 