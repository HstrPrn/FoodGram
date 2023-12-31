from django_filters import FilterSet, filters

from .models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    is_favorited = filters.NumberFilter(
        method='is_favorited_filter',
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='is_in_shopping_cart_filter',
    )

    def is_favorited_filter(self, qs, name, value):
        if value and self.request.user.is_authenticated:
            return qs.filter(in_favorites__user=self.request.user)
        return qs

    def is_in_shopping_cart_filter(self, qs, name, value):
        if value and self.request.user.is_authenticated:
            return qs.filter(in_cart__user=self.request.user)
        return qs

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )
