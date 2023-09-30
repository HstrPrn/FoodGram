from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .filters import RecipeFilter
from .models import (
    Ingredient,
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
    RecipeShortSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from utils.permissions import IsAuthor
from utils.paginators import CustomPaginator
from utils.services import download_csv


User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюесет тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.prefetch_related(
        'tags', 'ingredients'
    ).select_related('author')
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

    def _post_action_view(self, request, pk=None, serializer=None):
        """Обработчик post запросов."""
        serializer_obj = serializer(
            data={'id': pk},
            context={'request': request}
        )
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        recipe = get_object_or_404(Recipe, pk=pk)
        return Response(
            RecipeShortSerializer(recipe).data,
            status=status.HTTP_201_CREATED
        )

    def _delete_action_view(
            self, request, pk=None, serializer=None, model=None):
        """Обработчик delete запросов."""
        serializer_obj = serializer(
            data={'id': pk},
            context={'request': request}
        )
        serializer_obj.is_valid(raise_exception=True)
        self.perform_destroy(model.objects.filter(**serializer_obj.data))

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self._post_action_view(request, pk, FavoriteSerializer)
        return self._delete_action_view(
            request, pk, FavoriteSerializer, Favorite
        )

    @action(
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self._post_action_view(request, pk, ShoppingCartSerializer)
        return self._delete_action_view(
            request, pk, ShoppingCartSerializer, ShoppingCart
        )

    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_cart__user=request.user
        ).select_related(
            'author'
        ).prefetch_related(
            'tags', 'ingredients'
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            amount=Sum('ingredient_quantity')
        )
        return download_csv(ingredients)
