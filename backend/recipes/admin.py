from django.contrib import admin

from .models import Recipe, Tag, Ingredient, RecipeIngredients


admin.site.register(RecipeIngredients)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
