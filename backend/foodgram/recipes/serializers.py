import re

from rest_framework import serializers

from .models import Tag


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
