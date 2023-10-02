import base64

from django.core.files.base import ContentFile
from django.db import transaction
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
from utils.services import check_unique


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

    def _get_user(self):
        return self.context.get('request').user

    def get_is_favorited(self, obj):
        user = self._get_user()
        return (
            user.is_authenticated
            and obj.in_favorites.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self._get_user()
        return (
            user.is_authenticated
            and obj.in_cart.filter(user=user).exists()
        )

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

    def validate(self, attrs):
        if not attrs.get('tags'):
            raise ValidationError({
                'error': 'Добавьте тег.'
            })
        if not attrs.get('ingredients'):
            raise ValidationError({
                'error': 'Добавьте ингредиенты.'
            })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = self.Meta.model.objects.create(
            **validated_data,
            author=self._get_user()
        )
        recipe.ingredient.set(
            self._create_recipe_ingredients_relations(recipe, ingredients)
        )
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
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
        instance.tags.set(check_unique(tags))
        instance.save()
        return instance

    def _create_recipe_ingredients_relations(self, recipe, ingredients):
        """
        Создание списка объектов в промежуточной таблице RecipeIngredient.
        """

        valid_data = check_unique(ingredients)
        return RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                ingredient_quantity=ingredient.get(
                    'ingredient_quantity'
                )) for ingredient in valid_data],

        )

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context=self.context
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор модели Recipe только для чтения"""
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

    def _is_exist(self, attrs):
        return self.Meta.model.objects.filter(
            recipe=attrs.get('id').id,
            user=self._get_user()
        ).exists()

    def _get_user(self):
        return self.context.get('request').user

    def validate(self, attrs, exist_message=None, not_exist_message=None):
        if all((
            not exist_message,
            not not_exist_message
        )):
            exist_message = 'Рецепт уже добавлен в избранное.'
            not_exist_message = 'Рецепт не найден в избранном.'
        if all((
            self._is_exist(attrs),
            self.context.get('request').method == 'POST'
        )):
            raise ValidationError({
                'error': exist_message
            })
        if all((
            not self._is_exist(attrs),
            self.context.get('request').method == 'DELETE'
        )):
            raise ValidationError({
                'error': not_exist_message
            })
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        obj = self.Meta.model.objects.create(
            recipe=validated_data.get('id'),
            user=self._get_user()
        )
        return obj

    class Meta:
        model = Favorite
        fields = ('id',)


class ShoppingCartSerializer(FavoriteSerializer):
    """Сериализатор корзины поккупок"""
    def validate(self, attrs):
        exist_message = 'Рецепт уже добавлен в список покупок.'
        not_exist_message = 'Рецепт не найден в списке покупок.'
        return super().validate(attrs, exist_message, not_exist_message)

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart
