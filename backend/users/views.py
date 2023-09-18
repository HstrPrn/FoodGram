from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from .serializers import UserSerializer
from utils.paginators import CustomPaginator
from .models import Follow
from .serializers import FollowSerializer


User = get_user_model()


class UserViewSet(BaseUserViewSet):
    pagination_class = CustomPaginator

    @action(
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        detail=True
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                data={'author_id': author.id,
                      'user': request.user.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Follow.objects.filter(
            user=request.user,
            author=author
        ).exists():
            raise ValidationError({
                'error': 'Пользователь уже удален из избранного'
            })
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
        queryset = Follow.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(
            FollowSerializer(queryset, many=True, context={'request': request})
        )
