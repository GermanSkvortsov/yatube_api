"""Сериализаторы для API приложения Yatube."""

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ['id', 'author', 'post', 'text', 'created']
        model = Comment
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')

        # Блокируем строку для атомарной проверки
        with transaction.atomic():
            exists = Follow.objects.select_for_update().filter(
                user=self.context['request'].user,
                following=value
            ).exists()
            if exists:
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя')

        return value
