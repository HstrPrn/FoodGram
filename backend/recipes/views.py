from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .filters import RecipeFilter
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
from .permissions import IsAuthor
from .utils import download_csv
from utils.paginators import CustomPaginator


User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPaginator
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = (AllowAny,)
        elif self.action == 'partial_update':
            self.permission_classes = (IsAuthor,)
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

        message = 'Рецепт не найден в списке покупок.'
        return self.__delete_action_view(
            request, pk, ShoppingCart, message
        )

    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_cart__user=request.user
        ).values('ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('ingredient_quantity')
        )
        return download_csv(ingredients)
