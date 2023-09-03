from django.contrib import admin

from .models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Favorite,
    PurchaseList,
)


admin.site.register(RecipeIngredient)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


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
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (IngredientInline,)

    def get_favorites_count(self, obj):
        return obj.favorites.all().count()

    get_favorites_count.short_description = 'Всего в избранном'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('recipe__name',)


@admin.register(PurchaseList)
class PurchaseListAdmin(admin.ModelAdmin):
    pass
