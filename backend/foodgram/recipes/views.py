from rest_framework import viewsets, permissions, filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import (
    Tag,
    Ingredient,
    Recipe,
    FavoriteRecipe,
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'author']
    filterset_fields = ['name', 'author']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user != instance.author:
            raise PermissionDenied('You cannot update this item')
        serializer.save()

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='favorite',
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = Recipe.objects.filter(pk=pk)
        if not recipe.exists():
            return Response({'detail': 'Recipe not exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = recipe[0]

        if request.method == 'DELETE':
            favorite = get_object_or_404(FavoriteRecipe,
                                         user=request.user,
                                         recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if FavoriteRecipe.objects.filter(user=request.user,
                                         recipe=recipe).exists():
            return Response({'detail': 'Already favorited'},
                            status=status.HTTP_400_BAD_REQUEST)

        FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
        return Response(
            {
                'id': recipe.id,
                'name': recipe.name,
                'image': request.build_absolute_uri(recipe.image.url),
                'cooking_time': recipe.cooking_time
            },
            status=status.HTTP_201_CREATED)
