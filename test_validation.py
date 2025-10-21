#!/usr/bin/env python
"""Test script to validate the file validation functionality"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append('C:\\Users\\DisCode\\Desktop\\socialmedia-app')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmediaproject.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from posts.utils import validate_image_file, validate_video_file

def test_validation():
    print("Testing file validation functions...")
    
    # Test valid image file
    try:
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        validate_image_file(image, max_size_mb=1)
        print("[OK] Valid image validation passed")
    except Exception as e:
        print(f"[ERROR] Valid image validation failed: {e}")
    
    # Test invalid extension
    try:
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'invalid file',
            content_type='text/plain'
        )
        validate_image_file(invalid_file)
        print("[ERROR] Invalid extension validation failed - should have raised error")
    except Exception as e:
        print(f"[OK] Invalid extension validation passed: {type(e).__name__}")
    
    # Test valid video file
    try:
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        validate_video_file(video, max_size_mb=1)
        print("[OK] Valid video validation passed")
    except Exception as e:
        print(f"[ERROR] Valid video validation failed: {e}")

if __name__ == "__main__":
    test_validation()