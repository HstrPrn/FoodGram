from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Ingredient, Tag, Recipe, Favorite
from . serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
    RecipeShortSerializer,
)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    @action(
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True,
        url_name='favorite-create',
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if self.request.method == 'POST':
            serializer = RecipeShortSerializer(
                recipe,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(
                user=self.request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=201)
        Favorite.objects.filter(
            user=self.request.user,
            recipe=recipe
        ).delete()
        return Response(status=204)
