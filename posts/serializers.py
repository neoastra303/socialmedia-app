from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    reactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'created_at', 'author', 'comments', 'reactions_count']

    def get_reactions_count(self, obj):
        return obj.total_reactions()