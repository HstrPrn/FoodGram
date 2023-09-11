from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseCreateSerializer,
)
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class User:
    pass


class UserSerializer(BaseUserSerializer):
    """Сериализатор для кастомной модели пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def _get_user(self):
        return self.context.get('request').user

    def get_is_subscribed(self, obj):
        user = self._get_user()
        if not user.is_authenticated or user == obj:
            return False
        return user.follower.filter(author=obj).exists()

    def create(self, validated_data):
        user = User(**validated_data)
        return user
