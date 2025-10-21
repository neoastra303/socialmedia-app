from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment
from django.core.exceptions import ValidationError
from .utils import validate_image_file, validate_video_file


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('ماذا يدور في ذهنك؟'),
                'rows': 3,
                'maxlength': 5000
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) == 0:
            raise ValidationError(_('Post content cannot be empty or just whitespace.'))
        return content
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (10MB max)
            max_size = 10 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError(_('Image file too large. Size should not exceed 10MB.'))
            
            # Check file type
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            extension = '.' + image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError(_('Invalid image format. Valid formats are: .jpg, .jpeg, .png, .gif.'))
        return image
    
    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            # Check file size (100MB max)
            max_size = 100 * 1024 * 1024
            if video.size > max_size:
                raise ValidationError(_('Video file too large. Size should not exceed 100MB.'))
            
            # Check file type
            valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
            extension = '.' + video.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError(_('Invalid video format. Valid formats are: .mp4, .mov, .avi, .mkv, .webm.'))
        return video
    
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        
        # Validate that either content, image, or video is provided
        if not content and not image and not video:
            raise ValidationError(_('A post must have content, an image, or a video.'))
        
        # Validate that both image and video are not provided at the same time
        if image and video:
            raise ValidationError(_('A post cannot have both an image and a video.'))
        
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('اكتب تعليقك هنا...'),
                'rows': 3,
                'maxlength': 1000
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) == 0:
            raise ValidationError(_('Comment content cannot be empty or just whitespace.'))
        return content 