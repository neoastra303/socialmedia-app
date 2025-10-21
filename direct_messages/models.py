from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation between {', '.join([p.username for p in self.participants.all()])}"

    @classmethod
    def get_or_create_for_users(cls, user1, user2):
        # Get existing conversation or create new one
        conversation = cls.objects.filter(participants=user1).filter(participants=user2).first()
        if not conversation:
            conversation = cls.objects.create()
            conversation.participants.add(user1, user2)
        return conversation, not conversation.pk  # Return (conversation, created)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(
        max_length=5000,
        validators=[MinLengthValidator(1, message="Message content cannot be empty.")]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def clean(self):
        """Custom validation for the Message model"""
        super().clean()
        if self.content and len(self.content.strip()) < 1:
            raise ValidationError("Message content cannot be empty or just whitespace.")
        
        if len(self.content) > 5000:
            raise ValidationError("Message content cannot exceed 5000 characters.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
