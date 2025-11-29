from rest_framework import viewsets, permissions, filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import (
    Tag,
    Ingredient,
    Recipe,
    FavoriteRecipe,
    ShoppingCart,
)

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
)

from .filters import RecipeFilter

from .pagination import DefaultPagination

from .utils import recipes_to_csv


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'author']
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == '1' and not user.is_anonymous:
            recipes_favorited = [
                favorite.recipe
                for favorite in FavoriteRecipe.objects.filter(user=user)
            ]
            queryset = Recipe.objects.filter(
                id__in=[r.id for r in recipes_favorited])

        is_in_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_in_cart == '1' and not user.is_anonymous:
            recipes_in_cart = [
                shopping_cart.recipe
                for shopping_cart in ShoppingCart.objects.filter(user=user)
            ]
            queryset = Recipe.objects.filter(
                id__in=[r.id for r in recipes_in_cart])

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user != instance.author:
            raise PermissionDenied('You cannot update this item')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('You cannot delete this item')
        super().perform_destroy(instance)

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
            favorite = FavoriteRecipe.objects.filter(user=request.user,
                                                     recipe=recipe)
            if not favorite.exists():
                return Response({'detail': 'Not in favorites'},
                                status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=True,
            methods=['post', 'delete'],
            url_path='shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = Recipe.objects.filter(pk=pk)
        if not recipe.exists():
            return Response({'detail': 'Recipe not exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = recipe[0]

        if request.method == 'DELETE':
            shopping_cart = ShoppingCart.objects.filter(user=request.user,
                                                        recipe=recipe)
            if not shopping_cart.exists():
                return Response({'detail': 'Not in shopping cart'},
                                status=status.HTTP_400_BAD_REQUEST)

            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if ShoppingCart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            return Response({'detail': 'Already in shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)

        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        return Response(
            {
                'id': recipe.id,
                'name': recipe.name,
                'image': request.build_absolute_uri(recipe.image.url),
                'cooking_time': recipe.cooking_time
            },
            status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get'],
            url_path='download_shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        recipes = [
            shopping_cart.recipe
            for shopping_cart in ShoppingCart.objects.filter(user=request.user)
        ]
        csv_string = recipes_to_csv(recipes)
        response = HttpResponse(csv_string,
                                content_type='text/csv',
                                headers={
                                    'Content-Disposition':
                                    'attachment; filename="shopping_cart.csv"'
                                })
        return response
