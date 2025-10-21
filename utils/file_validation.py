import os
from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_file(value):
    """
    Validate image file format and size
    """
    # Check file size (max 10MB for general images)
    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'الملف كبير جداً. الحد الأقصى للحجم هو 10 ميغابايت.')

    # Check file format
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'نوع الملف غير مدعوم. أنواع الملفات المدعومة: {", ".join(valid_extensions)}')
    
    # Verify it's actually an image
    try:
        Image.open(value).verify()
    except Exception:
        raise ValidationError('الملف ليس صورة صالحة.')


def validate_profile_image(value):
    """
    Validate profile image file format and size
    """
    # Check file size (max 5MB for profile images)
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'صورة الملف الشخصي كبيرة جداً. الحد الأقصى للحجم هو 5 ميغابايت.')

    # Check file format
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'نوع صورة الملف الشخصي غير مدعوم. أنواع الملفات المدعومة: {", ".join(valid_extensions)}')
    
    # Verify it's actually an image
    try:
        Image.open(value).verify()
    except Exception:
        raise ValidationError('ملف الصورة غير صالح.')


def validate_story_image(value):
    """
    Validate story image file format and size
    """
    # Check file size (max 20MB for story images)
    max_size = 20 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'صورة القصة كبيرة جداً. الحد الأقصى للحجم هو 20 ميغابايت.')

    # Check file format
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'نوع صورة القصة غير مدعوم. أنواع الملفات المدعومة: {", ".join(valid_extensions)}')
    
    # Verify it's actually an image
    try:
        Image.open(value).verify()
    except Exception:
        raise ValidationError('ملف صورة القصة غير صالح.')


def validate_story_video(value):
    """
    Validate story video file format and size
    """
    # Check file size (max 100MB for story videos)
    max_size = 100 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'فيديو القصة كبير جداً. الحد الأقصى للحجم هو 100 ميغابايت.')

    # Check file format
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'نوع فيديو القصة غير مدعوم. أنواع الملفات المدعومة: {", ".join(valid_extensions)}')