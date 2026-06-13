from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os
from background_task import background
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class Profile(models.Model):
    """
    User profile model containing additional information about the user.

    Attributes:
        user (OneToOneField): Reference to the associated User model
        bio (TextField): User's biography, max length 500 characters
        location (CharField): User's location, max length 100 characters
        birth_date (DateField): User's date of birth
        profile_picture (ImageField): User's profile picture
        followers (ManyToManyField): Users following this profile
        created_at (DateTimeField): Timestamp when the profile was created
        updated_at (DateTimeField): Timestamp when the profile was last updated
        email_verified (BooleanField): Whether the user's email is verified
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default.jpg', 
        upload_to='profile_pics',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        """String representation of the Profile model."""
        return f'{self.user.username} Profile'

    def clean(self):
        """Custom validation for the Profile model"""
        super().clean()
        if self.bio and len(self.bio) > 500:
            raise ValidationError("Bio cannot exceed 500 characters.")
        
        if self.location and len(self.location) > 100:
            raise ValidationError("Location cannot exceed 100 characters.")
        
        if self.image and self.image.size:
            max_size = 5 * 1024 * 1024  # 5MB
            if self.image.size > max_size:
                raise ValidationError(f'Profile image too large. Size should not exceed 5MB.')

    def save(self, *args, **kwargs):
        self.full_clean()
        image_changed = False
        if self.pk and self.image:
            try:
                original = Profile.objects.get(pk=self.pk).image
                image_changed = (original != self.image)
            except Profile.DoesNotExist:
                image_changed = bool(self.image)
        else:
            image_changed = bool(self.image)
        super().save(*args, **kwargs)
        if image_changed:
            from .tasks import process_profile_image
            process_profile_image(self.id, schedule=0)

    def follow(self, user):
        if user == self.user:
            return False
        try:
            self.following.add(user.profile)
            return True
        except Profile.DoesNotExist:
            return False

    def unfollow(self, user):
        self.following.remove(user.profile)
        return True

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()




