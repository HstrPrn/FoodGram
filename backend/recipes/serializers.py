from rest_framework.serializers import ModelSerializer

from .models import Ingredient, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'measurement_unit',
        )
