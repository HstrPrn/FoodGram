from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer, FollowingUserSerializer
from utils.paginators import CustomPaginator


User = get_user_model()


class UserViewSet(BaseUserViewSet):
    """Вьюсет пользователей и подписок"""
    pagination_class = CustomPaginator

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (CurrentUserOrAdmin,)
        return super().get_permissions()

    @action(
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={'id': author.id},
            context={'request': request}
        )
        if request.method == 'POST':
            serializer = FollowSerializer(
                data={'id': author.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                FollowingUserSerializer(
                    author,
                    context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED)

        serializer.is_valid(raise_exception=True)
        Follow.objects.filter(
            user=request.user,
            author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowingUserSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(
            FollowingUserSerializer(
                queryset, many=True,
                context={'request': request}
            )
        )
