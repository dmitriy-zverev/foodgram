from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    color = models.CharField(max_length=7, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
