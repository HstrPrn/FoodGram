from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


User = get_user_model()


class Recipe(models.Model):
    tag = models.ForeignKey(
        'Tag',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='recipes',
        verbose_name='Список тегов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    ingridient = models.ManyToManyField(
        'Ingridient',
        through='RecipeIngridients',
        verbose_name='Ингридиенты',
        related_name='+'
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранном'
    )
    is_in_shoping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe',
        blank=True,                 # сделать обязательным
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Время готовки'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=200,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг'
    )

    class Meta:
        pass

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Ingridient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class RecipeIngridients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    ingredient_quantity = models.IntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Колличество ингридиента'
    )
