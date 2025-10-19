from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('ماذا يدور في ذهنك؟')
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('اكتب تعليقك هنا...'),
                'rows': 3
            })
        } 