from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Reaction, Hashtag

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
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
