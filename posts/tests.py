from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Post, Reaction, Hashtag, Story
from .forms import PostForm
from .utils import validate_image_file, validate_video_file
from django.core.files.base import ContentFile
import tempfile

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.post = Post.objects.create(author=self.user, content='Test post')

    def test_post_creation(self):
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.content, 'Test post')
        self.assertEqual(self.post.total_reactions(), 0)

    def test_reaction(self):
        reaction = Reaction.objects.create(post=self.post, user=self.user, reaction_type='like')
        self.assertEqual(self.post.total_reactions(), 1)
        self.assertEqual(self.post.user_reaction(self.user), 'like')

    def test_hashtag(self):
        hashtag = Hashtag.objects.create(name='testtag')
        self.post.hashtags.add(hashtag)
        self.assertIn(hashtag, self.post.hashtags.all())


class PostFileValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
    def test_image_validation_success(self):
        """Test that valid image files pass validation"""
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        # Should not raise validation error
        try:
            validate_image_file(image, max_size_mb=1)
        except ValidationError:
            self.fail("Valid image file raised ValidationError")

    def test_video_validation_success(self):
        """Test that valid video files pass validation"""
        video = SimpleUploadedFile(
            name='test_video.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        # Should not raise validation error
        try:
            validate_video_file(video, max_size_mb=1)
        except ValidationError:
            self.fail("Valid video file raised ValidationError")

    def test_invalid_image_extension(self):
        """Test that invalid image extensions fail validation"""
        invalid_image = SimpleUploadedFile(
            name='test_bad.txt',
            content=b'invalid file',
            content_type='text/plain'
        )
        
        with self.assertRaises(ValidationError):
            validate_image_file(invalid_image)

    def test_invalid_video_extension(self):
        """Test that invalid video extensions fail validation"""
        invalid_video = SimpleUploadedFile(
            name='test_bad.txt',
            content=b'invalid file',
            content_type='text/plain'
        )
        
        with self.assertRaises(ValidationError):
            validate_video_file(invalid_video)

    def test_large_image_file(self):
        """Test that large image files fail validation"""
        large_image = SimpleUploadedFile(
            name='large_image.jpg',
            content=b'x' * (2 * 1024 * 1024),  # 2MB file
            content_type='image/jpeg'
        )
        
        with self.assertRaises(ValidationError):
            validate_image_file(large_image, max_size_mb=1)  # 1MB limit

    def test_large_video_file(self):
        """Test that large video files fail validation"""
        large_video = SimpleUploadedFile(
            name='large_video.mp4',
            content=b'x' * (102 * 1024 * 1024),  # 102MB file
            content_type='video/mp4'
        )
        
        with self.assertRaises(ValidationError):
            validate_video_file(large_video, max_size_mb=100)  # 100MB limit


class PostFormValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_post_form_valid_with_image(self):
        """Test that post form accepts valid image uploads"""
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        
        form_data = {'content': 'Test content'}
        form_files = {'image': image}
        
        form = PostForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_post_form_valid_with_video(self):
        """Test that post form accepts valid video uploads"""
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        
        form_data = {'content': 'Test content'}
        form_files = {'video': video}
        
        form = PostForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_post_form_invalid_both_image_and_video(self):
        """Test that post form rejects having both image and video"""
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        
        form_data = {'content': 'Test content'}
        form_files = {'image': image, 'video': video}
        
        form = PostForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('A post cannot have both an image and a video.', form.non_field_errors())

    def test_post_form_invalid_no_content_or_media(self):
        """Test that post form requires content or media"""
        form_data = {'content': ''}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('A post must have content, an image, or a video.', form.non_field_errors())


class PostModelValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_post_model_valid_with_video(self):
        """Test that post model accepts video uploads"""
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        
        post = Post(
            author=self.user,
            content='Test content with video',
            video=video
        )
        
        # This should not raise ValidationError
        try:
            post.full_clean()
            post.save()
        except ValidationError:
            self.fail("Valid post with video raised ValidationError")

    def test_post_model_invalid_both_image_and_video(self):
        """Test that post model rejects both image and video"""
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        
        post = Post(
            author=self.user,
            content='Test content',
            image=image,
            video=video
        )
        
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_post_model_max_video_size(self):
        """Test that post model validates video size"""
        # Create a large video file (101MB)
        large_video = SimpleUploadedFile(
            name='large_video.mp4',
            content=b'x' * (101 * 1024 * 1024),  # 101MB
            content_type='video/mp4'
        )
        
        post = Post(
            author=self.user,
            content='Test content with large video',
            video=large_video
        )
        
        with self.assertRaises(ValidationError):
            post.full_clean()


class PostViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_post_creation_with_image(self):
        """Test creating a post with an image"""
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        
        response = self.client.post(reverse('posts:post_create'), {
            'content': 'Test post with image',
            'image': image
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Post.objects.filter(content='Test post with image').exists())

    def test_post_creation_with_video(self):
        """Test creating a post with a video"""
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        
        response = self.client.post(reverse('posts:post_create'), {
            'content': 'Test post with video',
            'video': video
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Post.objects.filter(content='Test post with video').exists())

    def test_post_creation_with_both_image_and_video_fails(self):
        """Test that creating a post with both image and video fails"""
        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )
        video = SimpleUploadedFile(
            name='test.mp4',
            content=b'test video content',
            content_type='video/mp4'
        )
        
        response = self.client.post(reverse('posts:post_create'), {
            'content': 'Test post with both',
            'image': image,
            'video': video
        })
        
        self.assertEqual(response.status_code, 200)  # Should return to form with errors
        self.assertContains(response, 'A post cannot have both an image and a video.')
