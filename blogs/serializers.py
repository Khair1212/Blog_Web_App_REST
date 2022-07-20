from django.conf import settings
from django.db import models
from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    # Create a custom method field

    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # post = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'status', 'created')


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ('id', 'title', 'description', 'status')
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'created')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'modified')

class PostShareSerializer(serializers.Serializer):
    email = serializers.ListField()

    class Meta:
        fields = ['email']

