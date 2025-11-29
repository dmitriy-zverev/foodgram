from django_filters import rest_framework as filters
from .models import Recipe


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug',
                              method='filter_tags_all')

    def filter_tags_all(self, queryset, name, value):
        tags_slugs = self.request.query_params.getlist('tags')

        if not tags_slugs:
            return queryset

        return queryset.filter(tags__slug__in=tags_slugs).distinct()

    class Meta:
        model = Recipe
        fields = ['name', 'author', 'tags']
