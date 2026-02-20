"""Сериализаторы для API приложения Yatube."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    user_id = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following', 'user_id')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user_id', 'following'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate_following(self, value):
        """Проверка на подписку на самого себя."""
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return value

    def create(self, validated_data):
        """Создание подписки с текущим пользователем."""
        validated_data.pop('user_id', None)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
