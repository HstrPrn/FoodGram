from django.contrib import admin

from .models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)


admin.site.register(RecipeIngredient)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    verbose_name = 'Тег рецепта'
    verbose_name_plural = 'Теги рецепта'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'get_favorites_count',
    )
    exclude = ('tags',)
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (
        IngredientInline,
        TagInline,
    )

    def get_favorites_count(self, obj):
        return obj.in_favorites.count()

    get_favorites_count.short_description = 'Всего в избранном'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('recipe__name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
