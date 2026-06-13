from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import os

class Hashtag(models.Model):
    """
    Hashtag model
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Post model for the application
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(validators=[MinLengthValidator(1, message="Post content cannot be empty.")])
    image = models.ImageField(upload_to='posts/', blank=True, null=True, 
                             validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    video = models.FileField(upload_to='posts/', blank=True, null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv', 'webm'])])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')

    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"

    def total_reactions(self):
        return self.reactions.count()

    def user_reaction(self, user):
        try:
            return self.reactions.get(user=user).reaction_type
        except Reaction.DoesNotExist:
            return None

    def clean(self):
        # Validate that either content, image, or video is provided
        if not self.content and not self.image and not self.video:
            raise ValidationError('A post must have content, an image, or a video.')
        
        # Validate content length
        if self.content and len(self.content.strip()) < 1:
            raise ValidationError('Post content cannot be empty.')
        
        # Validate that both image and video are not provided at the same time
        if self.image and self.video:
            raise ValidationError('A post cannot have both an image and a video.')
        
        # Validate image size if provided
        if self.image:
            max_size = 10 * 1024 * 1024  # 10MB
            if self.image.size > max_size:
                raise ValidationError(f'Image file too large. Size should not exceed 10MB.')
        
        # Validate video size if provided
        if self.video:
            max_size = 100 * 1024 * 1024  # 100MB
            if self.video.size > max_size:
                raise ValidationError(f'Video file too large. Size should not exceed 100MB.')
    
    def save(self, *args, **kwargs):
        self.full_clean()  # This runs the clean method
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class Reaction(models.Model):
    """
    Reaction model for posts
    """
    LIKE = 'like'
    LOVE = 'love'
    LAUGH = 'laugh'
    ANGRY = 'angry'
    SAD = 'sad'

    REACTION_CHOICES = [
        (LIKE, '👍 إعجاب'),
        (LOVE, '❤️ حب'),
        (LAUGH, '😂 ضحك'),
        (ANGRY, '😠 غضب'),
        (SAD, '😢 حزن'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES, default=LIKE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')  # One reaction per user per post

    def __str__(self):
        return f"{self.user.username} - {self.reaction_type} on {self.post.id}"

class Story(models.Model):
    """
    Temporary stories model
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    content = models.TextField(
        blank=True, 
        max_length=2000,
        validators=[MinLengthValidator(1, message="Story content cannot be empty when provided.")]
    )
    image = models.ImageField(
        upload_to='stories/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    video = models.FileField(
        upload_to='stories/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])]
    )
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()  # 24 hours from creation
    views = models.ManyToManyField(User, related_name='viewed_stories', blank=True)

    def __str__(self):
        return f"{self.author.username} - Story"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def clean(self):
        """Custom validation for the Story model"""
        super().clean()
        # Validate that either content, image, or video is provided
        if not self.content.strip() and not self.image and not self.video:
            raise ValidationError('A story must have content, an image, or a video.')
        
        # Validate content length
        if self.content and len(self.content.strip()) > 2000:
            raise ValidationError('Story content cannot exceed 2000 characters.')
        
        # Validate that both image and video are not provided at the same time
        if self.image and self.video:
            raise ValidationError('A story cannot have both an image and a video.')
        
        # Validate file sizes
        if self.image and self.image.size:
            max_size = 20 * 1024 * 1024  # 20MB
            if self.image.size > max_size:
                raise ValidationError(f'Image file too large. Size should not exceed 20MB.')
        
        if self.video and self.video.size:
            max_size = 100 * 1024 * 1024  # 100MB
            if self.video.size > max_size:
                raise ValidationError(f'Video file too large. Size should not exceed 100MB.')

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    """
    Comment model for posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(
        max_length=1000,
        validators=[MinLengthValidator(1, message="Comment content cannot be empty.")]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.author.username} on {self.post.id}"

    def clean(self):
        """Custom validation for the Comment model"""
        super().clean()
        if self.content and len(self.content.strip()) < 1:
            raise ValidationError("Comment content cannot be empty or just whitespace.")
        
        if len(self.content) > 1000:
            raise ValidationError("Comment content cannot exceed 1000 characters.")
        
        # Validate that a comment cannot be its own parent
        if self.pk and self.parent and self.parent.pk == self.pk:
            raise ValidationError("A comment cannot be a reply to itself.")
        
        # Validate that the parent comment belongs to the same post
        if self.parent and self.parent.post != self.post:
            raise ValidationError("Reply must belong to the same post as parent comment.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.id}"
