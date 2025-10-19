from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

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
