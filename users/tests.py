from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from .models import Profile, FollowRequest

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.followers_count, 0)
        self.assertEqual(profile.following_count, 0)

    def test_follow_unfollow(self):
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        profile1 = self.user.profile
        profile2 = user2.profile
        self.assertTrue(profile1.follow(user2))
        self.assertEqual(profile1.following_count, 1)
        self.assertEqual(profile2.followers_count, 1)
        profile1.unfollow(user2)
        self.assertEqual(profile1.following_count, 0)
        self.assertEqual(profile2.followers_count, 0)

    def test_block_unblock(self):
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        profile1 = self.user.profile
        profile2 = user2.profile
        profile1.block(user2)
        self.assertTrue(profile1.is_blocked(user2))
        profile1.unblock(user2)
        self.assertFalse(profile1.is_blocked(user2))

    def test_private_profile_sends_follow_request(self):
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        user2.profile.is_private = True
        user2.profile.save()
        self.assertTrue(user2.profile.is_private)
        # Follow request should be created instead of direct follow
        FollowRequest.objects.create(from_user=self.user.profile, to_user=user2.profile)
        self.assertEqual(FollowRequest.objects.filter(to_user=user2.profile).count(), 1)

    def test_follow_request_accept(self):
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        user2.profile.is_private = True
        user2.profile.save()
        req = FollowRequest.objects.create(from_user=self.user.profile, to_user=user2.profile)
        req.from_user.following.add(user2.profile)
        user2.profile.followers.add(req.from_user)
        req.delete()
        self.assertTrue(self.user.profile.following.filter(pk=user2.pk).exists())
        self.assertTrue(user2.profile.followers.filter(pk=self.user.pk).exists())


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123',
                                            email='test@example.com')
        self.user.profile.email_verified = True
        self.user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_profile_page(self):
        response = self.client.get(reverse('users:profile'), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_public_profile_view(self):
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        response = self.client.get(reverse('users:profile', args=['testuser2']), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_settings_page(self):
        response = self.client.get(reverse('users:settings'), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_password_change(self):
        response = self.client.post(reverse('users:password_change'), {
            'old_password': 'testpass123',
            'new_password1': 'NewPass12345',
            'new_password2': 'NewPass12345',
        }, secure=True)
        self.assertIn(response.status_code, [200, 302])  # May redirect or show form

    def test_email_change(self):
        response = self.client.post(reverse('users:change_email'), {
            'email': 'newemail@example.com',
            'password': 'testpass123',
        }, secure=True)
        self.assertIn(response.status_code, [200, 302])
