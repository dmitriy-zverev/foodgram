import re
import base64

from rest_framework import serializers

from django.core.files.base import ContentFile

from .models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeToIngredient,
)

from users.serializers import (UserSerializer)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

    def validate(self, attrs):
        slug = attrs.get('slug')
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise serializers.ValidationError(
                {'slug': 'Неверный формат слага'})

        color = attrs.get('color')
        if not re.match(r'#[0-9a-fA-F]{6}', color):
            raise serializers.ValidationError(
                {'color': 'Неверный формат цвета'})


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=True)
    ingredients = serializers.StringRelatedField(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    author = UserSerializer(required=False)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'tags', 'ingredients', 'image', 'name',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')
        read_only_fields = ('author', 'id', 'is_favorited',
                            'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False

    def validate_tags(self, value):
        return value

    def validate_ingredients(self, value):
        return value

    def validate(self, attrs):
        tags = attrs.get('tags')
        if tags is None or tags == []:
            raise serializers.ValidationError({'tags': 'Required field'})

        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                {'tags': 'Repeated items not allowed'})

        cooking_time = attrs.get('cooking_time')
        if cooking_time <= 0:
            raise serializers.ValidationError(
                {'cooking_time': 'Must be greater than zero'})

        return super().validate(attrs)

    def create(self, validated_data):
        recipe = super().create(validated_data)

        ingredients = self.initial_data.get('ingredients')
        if ingredients is None or ingredients == []:
            raise serializers.ValidationError(
                {'ingredients': 'Required field'})

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.filter(id=ingredient['id'])
            if not current_ingredient.exists():
                raise serializers.ValidationError(
                    {'ingredients': 'Not exists'})
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    {'ingredients': {
                        'amount': 'Must be greater then zero'
                    }})
            if RecipeToIngredient.objects.filter(
                    recipe=recipe, ingredient=current_ingredient[0]).exists():
                raise serializers.ValidationError(
                    {'ingredients': 'Repeated ingredients'})
            RecipeToIngredient.objects.create(recipe=recipe,
                                              ingredient=current_ingredient[0],
                                              amount=ingredient['amount'])
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        instance.tags.set(tags)

        ingredients = self.initial_data.get('ingredients')
        if ingredients is None or ingredients == []:
            raise serializers.ValidationError(
                {'ingredients': 'Required field'})

        RecipeToIngredient.objects.filter(recipe=instance).delete()

        seen_ingredient_ids = set()
        for ingredient in ingredients:
            ingredient_id = ingredient['id']

            if ingredient_id in seen_ingredient_ids:
                raise serializers.ValidationError(
                    {'ingredients': 'Repeated ingredients'})
            seen_ingredient_ids.add(ingredient_id)

            current_ingredient = Ingredient.objects.filter(id=ingredient_id)
            if not current_ingredient.exists():
                raise serializers.ValidationError(
                    {'ingredients': 'Not exists'})

            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    {'ingredients': {
                        'amount': 'Must be greater then zero'
                    }})

            RecipeToIngredient.objects.create(recipe=instance,
                                              ingredient=current_ingredient[0],
                                              amount=ingredient['amount'])

        instance.refresh_from_db()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['tags'] = TagSerializer(instance.tags.all(), many=True).data

        recipe_ingredients = RecipeToIngredient.objects.filter(
            recipe=instance).select_related('ingredient')

        ingredient_data = []
        for obj in recipe_ingredients:
            current_ingredient = {
                'id': obj.ingredient.id,
                'name': obj.ingredient.name,
                'measurement_unit': obj.ingredient.measurement_unit,
                'amount': obj.amount,
            }
            ingredient_data.append(current_ingredient)

        data['ingredients'] = ingredient_data

        return data
