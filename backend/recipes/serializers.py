import base64

from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.db.models import F
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import (
    Ingredient,
    Tag,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart
)
from users.serializers import UserReadSerializer


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для обработки изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredients."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериальзатор для чтения модели Recipe."""

    tags = TagSerializer(many=True, read_only=True)

    author = UserReadSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def _get_user(self):
        return self.context.get('request').user

    def get_is_favorited(self, obj):
        user = self._get_user()
        if (user.is_authenticated
           and user.favorites.filter(recipe=obj).exists()):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self._get_user()
        if (user.is_authenticated
           and user.cart.filter(recipe=obj).exists()):
            return True
        return False

    def get_ingredients(self, obj):
        """
        Получение полей модели Ingredients с дополнительным полем amount
        из связанной таблицы RecipeIngredient.
        """

        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__ingredient_quantity')
        )


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной таблицы RecipeIngredient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )
        extra_kwargs = {
            'amount': {'source': 'ingredient_quantity'},
        }


class RecipeCreateSerializer(RecipeReadSerializer):
    """Сериализатор для создания, изменения и удаления модели Recipe."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )
    ingredients = RecipeIngredientsSerializer(many=True, required=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data,
            author=super()._get_user()
        )
        recipe.ingredient.set(
            self._create_recipe_ingredients_relations(recipe, ingredients)
        )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.ingredients.clear()
        instance.ingredient.set(
            self._create_recipe_ingredients_relations(instance, ingredients)
        )
        instance.tags.set(tags)
        instance.save()
        return instance

    def _create_recipe_ingredients_relations(self, recipe, ingredients):
        """
        Создание списка объектов в промежуточной таблице RecipeIngredient.
        """
        try:
            return RecipeIngredient.objects.bulk_create(
                    [RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient.get('id'),
                        ingredient_quantity=ingredient.get(
                            'ingredient_quantity'
                        )) for ingredient in ingredients]
            )
        except IntegrityError:
            raise ValidationError({
                'error': 'Ингредиент уже добавле в рецепт'
            })

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context=self.context
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = fields


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели избранных рецептов"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True
    )
    recipe = RecipeShortSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = (
            'recipe',
            'id',
        )

    def create(self, validated_data, message=None):
        if message is None:
            message = 'Рецепт уже добавлен в избранное.'
        try:
            return self.Meta.model.objects.create(
                recipe=validated_data.get('id'),
                user=self.context.get('request').user
            )
        except IntegrityError:
            raise ValidationError({
                'error': message
            })


class ShoppingCartSerializer(FavoriteSerializer):
    """Сериализатор корзины поккупок"""
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart

    def create(self, validated_data):
        message = 'Рецепт уже добавлен в список покупок.'
        return super().create(validated_data, message)
