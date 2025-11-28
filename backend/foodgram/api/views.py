from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404

from djoser.serializers import SetPasswordSerializer

from users.serializers import (
    UserSerializer,
    UserCreateSerializer,
    FollowSerializer,
)

from users.models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method.lower() == 'get':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserCreateSerializer(request.user,
                                          data=request.data,
                                          partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False,
            methods=['post'],
            url_path='set_password',
            permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']

        user = request.user
        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='subscribe',
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk=None):
        recipes_limit = request.query_params.get(
            'recipes_limit', settings.REST_FRAMEWORK['PAGE_SIZE'])
        recipes_limit = int(
            recipes_limit
        ) if recipes_limit else settings.REST_FRAMEWORK['PAGE_SIZE']

        author = get_object_or_404(User, pk=pk)
        if author == request.user:
            return Response({'author': 'Cannot follow yourself'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            follow = Follow.objects.filter(author=author,
                                           follower=request.user)
            if not follow.exists():
                return Response(
                    {'detail': 'Cannot unsubscribe when not subscribed'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow.delete()
            return Response({'detail': 'Unsubscribed'},
                            status=status.HTTP_204_NO_CONTENT)

        serializer = FollowSerializer(data=request.data,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, follower=request.user)

        author_recipes = author.recipes.select_related(
            'author')[:recipes_limit]

        response_data = {
            'id':
            author.id,
            'email':
            author.email,
            'username':
            author.username,
            'first_name':
            author.first_name,
            'last_name':
            author.last_name,
            'is_subscribed':
            True,
            'recipes': [{
                'id': recipe.id,
                'name': recipe.name,
                'image': request.build_absolute_uri(recipe.image.url),
                'cooking_time': recipe.cooking_time
            } for recipe in author_recipes],
            'recipes_count':
            len(author_recipes)
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get'],
            url_path='subscriptions',
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        limit = request.query_params.get('limit',
                                         settings.REST_FRAMEWORK['PAGE_SIZE'])
        limit = int(limit) if limit else settings.REST_FRAMEWORK['PAGE_SIZE']

        recipes_limit = request.query_params.get(
            'recipes_limit', settings.REST_FRAMEWORK['PAGE_SIZE'])
        recipes_limit = int(
            recipes_limit
        ) if recipes_limit else settings.REST_FRAMEWORK['PAGE_SIZE']

        queryset = Follow.objects.filter(follower=request.user)[:limit]

        queryset_data = []
        for item in queryset:
            author_recipes = item.author.recipes.select_related(
                'author')[:recipes_limit]
            queryset_data.append({
                'id':
                item.author.id,
                'email':
                item.author.email,
                'username':
                item.author.username,
                'first_name':
                item.author.first_name,
                'last_name':
                item.author.last_name,
                'is_subscribed':
                True,
                'recipes': [{
                    'id':
                    recipe.id,
                    'name':
                    recipe.name,
                    'image':
                    request.build_absolute_uri(recipe.image.url),
                    'cooking_time':
                    recipe.cooking_time
                } for recipe in author_recipes],
                'recipes_count':
                len(author_recipes)
            })

        page = self.paginate_queryset(queryset_data)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(queryset_data, status=status.HTTP_200_OK)
