from rest_framework.permissions import IsAuthenticated


class IsAuthor(IsAuthenticated):
    """Разрешение для автора рецепта."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
