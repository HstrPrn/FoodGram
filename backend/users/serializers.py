from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseCreateSerializer,
)
from rest_framework import serializers
from rest_framework.validators import ValidationError
from recipes.models import Recipe

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

    def _get_user(self):
        """Получение юзера."""
        return self.context.get('request').user

    def get_is_subscribed(self, obj):
        user = self._get_user()
        if any((
            not user.is_authenticated,
            user == obj
        )):
            return False
        return obj.following.filter(user=user).exists()

    class Meta(BaseUserSerializer.Meta):
        fields = ('is_subscribed',) + BaseUserSerializer.Meta.fields


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = fields


class FollowingUserSerializer(UserReadSerializer):
    """
    Сериализатор для модели пользователя(подписки) с дополнительно
    декларированными полями списка и колличества рецептов.
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def _get_recipes_limit(self):
        """Получение колличества выводимых рецептов из query_params."""
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            return int(limit)
        return None

    def get_recipes(self, obj):
        limit = self._get_recipes_limit()
        recipes = obj.recipes
        return RecipeSerializer(
            recipes, many=True, context=self.context
        ).data[:limit]

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def _create_follow(self, obj):
        user = self._get_user()
        return Follow.objects.create(
            user=user,
            author=obj
        )

    class Meta(UserReadSerializer.Meta):
        fields = (
            ('recipes', 'recipes_count') + UserReadSerializer.Meta.fields
        )
        read_only_fields = fields


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    def _get_user(self):
        return self.context.get('request').user

    def _is_exist(self, attrs):
        return self.Meta.model.objects.filter(
            author=attrs.get('id'),
            user=self._get_user()
        ).exists()

    def validate(self, attrs):
        if all((
            self._is_exist(attrs),
            self.context.get('request').method == 'POST'
        )):
            raise ValidationError({
                'error': 'Вы уже подписались на этого пользователя.'
            })
        elif all((
            not self._is_exist(attrs),
            self.context.get('request').method == 'DELETE'
        )):
            raise ValidationError({
                'error': 'Пользователь уже удален из избранного.'
            })
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        obj = self.Meta.model.objects.get_or_create(
            author=validated_data.get('id'),
            user=self.context.get('request').user
        )
        return obj

    class Meta:
        model = Follow
        fields = ('id',)
