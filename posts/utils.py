"""
Utility functions for file validation and handling
"""
import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_extension(file):
    """
    Validate file extension for images and videos
    """
    valid_extensions = {
        'image': ['.jpg', '.jpeg', '.png', '.gif'],
        'video': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    }
    
    # Get file extension
    _, ext = os.path.splitext(file.name)
    ext = ext.lower()
    
    # Check if extension is valid
    is_valid = any(ext in extensions for extensions in valid_extensions.values())
    
    if not is_valid:
        message = 'File type not supported. Valid formats are: %(valid_formats)s'
        raise ValidationError(
            _(message) % {
                'valid_formats': ', '.join(valid_extensions['image'] + valid_extensions['video'])
            }
        )

def validate_file_size(file, max_size_mb=10):
    """
    Validate file size
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    
    if file.size > max_size_bytes:
        message = 'File too large. Size should not exceed %(max_size)sMB.'
        raise ValidationError(
            _(message) % {
                'max_size': max_size_mb
            }
        )

def validate_image_file(file, max_size_mb=10):
    """
    Validate image file
    """
    validate_file_extension(file)
    
    # Verify it's an image extension
    valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    _, ext = os.path.splitext(file.name)
    ext = ext.lower()
    
    if ext not in valid_image_extensions:
        message = 'Invalid image format. Valid formats are: %(valid_formats)s'
        raise ValidationError(
            _(message) % {
                'valid_formats': ', '.join(valid_image_extensions)
            }
        )
    
    validate_file_size(file, max_size_mb)

def validate_video_file(file, max_size_mb=100):
    """
    Validate video file
    """
    validate_file_extension(file)
    
    # Verify it's a video extension
    valid_video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    _, ext = os.path.splitext(file.name)
    ext = ext.lower()
    
    if ext not in valid_video_extensions:
        message = 'Invalid video format. Valid formats are: %(valid_formats)s'
        raise ValidationError(
            _(message) % {
                'valid_formats': ', '.join(valid_video_extensions)
            }
        )
    
    validate_file_size(file, max_size_mb)

def get_file_type(file):
    """
    Determine if a file is an image or video based on extension
    """
    _, ext = os.path.splitext(file.name)
    ext = ext.lower()
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    
    if ext in image_extensions:
        return 'image'
    elif ext in video_extensions:
        return 'video'
    else:
        return 'unknown'