from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'recipes_count'
    )
    list_filter = (
        'username',
        'email',
    )

    def recipes_count(self, obj):
        return obj.recipes.all().count()

    recipes_count.short_description = 'Всего рецептов'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user',
    )
    search_fields = ('recipe__name',)
