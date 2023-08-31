from django.contrib import admin

from .models import Recipe, Tag, Ingridient, RecipeIngridients


admin.site.register(RecipeIngridients)


class IngridientInline(admin.TabularInline):
    model = Recipe.ingridient.through


@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RevipeAdmin(admin.ModelAdmin):
    inlines = (IngridientInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
