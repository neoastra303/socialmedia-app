from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
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
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    video = models.FileField(upload_to='stories/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()  # 24 hours from creation
    views = models.ManyToManyField(User, related_name='viewed_stories', blank=True)

    def __str__(self):
        return f"{self.author.username} - Story"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
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
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.author.username} on {self.post.id}"

    class Meta:
        ordering = ['created_at']
