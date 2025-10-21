from background_task import background
from django.apps import apps
from PIL import Image
import os

@background(schedule=0)
def process_profile_image(profile_id):
    try:
        Profile = apps.get_model('users', 'Profile')
        profile = Profile.objects.get(id=profile_id)
        if profile.image and os.path.exists(profile.image.path):
            img = Image.open(profile.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(profile.image.path)
            # Convert to WebP for better compression if possible
            try:
                img = Image.open(profile.image.path)
                webp_path = profile.image.path.rsplit('.', 1)[0] + '.webp'
                img.save(webp_path, 'WEBP', quality=80)
            except Exception:
                pass  # Fallback if WebP not supported
    except Profile.DoesNotExist:
        pass