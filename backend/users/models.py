from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from utils.regex import USERNAME_REGEX


class User(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Пользователь',
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Поле содержит недопустимые символы'
            )
        ]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='password'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        unique_together = ('username', 'email')

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Модель подписки пользователя на автора рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='following',
        verbose_name='Подписка'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_self_follow_constraint'
            ),
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow_constraint'
            ),
        )

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
