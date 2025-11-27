from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    color = models.CharField(max_length=7, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    measurement_unit = models.CharField(max_length=200,
                                        blank=False,
                                        null=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name='recipes')
    name = models.CharField(max_length=200, blank=False, null=False)
    image = models.ImageField(upload_to='foodgram/images/',
                              null=True,
                              default=None)
    text = models.TextField(blank=False, null=False)
    tags = models.ManyToManyField(Tag,
                                  blank=False,
                                  null=False,
                                  related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through="RecipeToIngredient",
                                         related_name="recipes")
    cooking_time = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class RecipeToIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name='recipetoingredients')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   blank=False,
                                   null=False,
                                   related_name='recipetoingredients')
    amount = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f'{self.recipe.name}: {self.ingredient.name} ({self.amount})'
