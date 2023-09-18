from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseCreateSerializer,
)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow


User = get_user_model()


class UserCreateSerializer(BaseCreateSerializer):
    """Сериализатор модели пользователя для записи."""

    class Meta(BaseCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = None


class UserReadSerializer(BaseUserSerializer):
    """Сериализатор модели пользователя для чтения."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('is_subscribed',) + BaseUserSerializer.Meta.fields

    def _get_user(self):
        """Получение юзера."""
        return self.context.get('request').user

    def get_is_subscribed(self, obj):
        user = self._get_user()
        if not user.is_authenticated or user == obj:
            return False
        return user.follower.filter(author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели подписок с дополнительно
    декларированными полями списка и колличества рецептов.
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    author = UserReadSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'author',
            'recipes',
            'recipes_count',
            'user',
            'author_id',
        )
        extra_kwargs = {
            'user': {'write_only': True},
            'author_id': {'write_only': True,
                          'source': 'author'},
        }
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого пользователя.'
            ),
        )

    def __get_recipes_limit(self):
        """Получение колличества выводимых рецептов из query_params."""
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            return int(limit)
        return None

    def get_recipes(self, obj):
        limit = self.__get_recipes_limit()
        return obj.author.recipes.values(
            'id',
            'name',
            'image',
            'cooking_time'
        )[:limit]

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
