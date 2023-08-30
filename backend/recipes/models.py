from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Recipe(models.Model):
    tags = models.ForeignKey(
        'Tags',
        on_delete=models.SET_DEFAULT,
        default=...,
        related_name='recipes',
        verbose_name='Список тегов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    ingridients = models.ManyToManyField(
        'Ingridients',
        through='RecipeIngridients',                # Написать модель
        verbose_name='Ингридиенты'
    )
    is_favorited = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='В избранном'
    )
    is_in_shoping_cart = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='В корзине',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe',
        blank=True,
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время готовки'
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=200,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )


class Ingridients(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = ...
