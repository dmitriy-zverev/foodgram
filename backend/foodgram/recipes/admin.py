from django.contrib import admin

from .models import (
    Recipe,
    Tag,
    Ingredient,
    FavoriteRecipe,
    ShoppingCart,
)

admin.site.register(Tag)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCart)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'favorite_count')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')

    def favorite_count(self, obj):
        in_favotites = len(FavoriteRecipe.objects.filter(recipe=obj))
        return in_favotites


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
