# flake8: noqa
from .models import RecipeToIngredient


def recipes_to_csv(recipes):
    ingredients = []

    for recipe in recipes:
        ingredients.extend(
            {
                'name': recipe.ingredient.name,
                'amount': recipe.amount,
                'measurement_unit': recipe.ingredient.measurement_unit,
            } for recipe in RecipeToIngredient.objects.filter(recipe=recipe))

    ingredients_len = len(ingredients)
    for i in range(ingredients_len - 1):
        ingredient = ingredients[i]
        for j in range(i + 1, ingredients_len):
            cur_ingredient = ingredients[j]
            if cur_ingredient['name'] == ingredient['name']:
                ingredient['amount'] += cur_ingredient['amount']
                ingredients.pop(j)
                ingredients_len -= 1

    csv_string = ''
    for ingredient in ingredients:
        csv_string += f'{ingredient['name']},{ingredient['amount']},{ingredient['measurement_unit']}\n'

    return csv_string
