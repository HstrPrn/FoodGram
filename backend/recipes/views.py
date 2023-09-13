from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
    RecipeIngredient,
)
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from .permissions import IsAuthorOrAdmin


User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializerializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializerializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializerializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = (AllowAny,)
        elif self.action == 'partial_update':
            self.permission_classes = (IsAuthorOrAdmin,)
        return super().get_permissions()

    def __post_action_view(self, request, pk=None, serializer_class=None):
        serializer = serializer_class(
            data={'id': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def __delete_action_view(self, request, pk=None, model=None, message=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if not model.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            raise ValidationError({
                'error': message
            })

        model.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.__post_action_view(request, pk, FavoriteSerializer)

        message = 'Рецепт не найден в избранном.'
        return self.__delete_action_view(request, pk, Favorite, message)

    @action(
        methods=('get', 'post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.__post_action_view(request, pk, ShoppingCartSerializer)
        elif request.method == 'DELETE':
            message = 'Рецепт не найден в списке покупок.'
            return self.__delete_action_view(
                request, pk, ShoppingCart, message
            )

    # @action(
    #     methods=('get', 'post', 'delete'),
    #     permission_classes=(IsAuthenticated,),
    #     detail=False
    # )
    # def download_shopping_card(self, request):
    #     recipes = request.user.favorites.all()
    #     ingredients = RecipeIngredient.objects.filter(


    #     )
    #     shopping_list = {}
        