from rest_framework import viewsets, permissions, filters

from .models import (Tag, Ingredient)

from .serializers import (TagSerializer, IngredientSerializer)


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
    search_fields = ['^name']
