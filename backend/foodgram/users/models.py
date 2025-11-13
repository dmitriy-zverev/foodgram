from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                null=False,
                                default='foodgram_user')
    email = models.EmailField(unique=True,
                              blank=False,
                              null=False,
                              max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Follow(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='follow_author')
    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='follow_follower')

    def __str__(self):
        return f'{self.follower.username} -> {self.author.username}'
