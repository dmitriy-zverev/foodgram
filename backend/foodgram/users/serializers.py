import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    first_name = serializers.CharField(required=True,
                                       allow_blank=False,
                                       max_length=150)
    last_name = serializers.CharField(required=True,
                                      allow_blank=False,
                                      max_length=150)
    username = serializers.CharField(required=True,
                                     allow_blank=False,
                                     max_length=150,
                                     validators=[
                                         UniqueValidator(
                                             queryset=User.objects.all(),
                                             message='User already exists')
                                     ])

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name',
                  'last_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 150,
            },
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                {'username': 'Contains invalid characters'})
        return value


class UserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False

        user = request.user
        if user.is_anonymous or user == obj:
            return False

        return Follow.objects.filter(author=obj, follower=user).exists()


class FollowSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    follower = UserSerializer(required=False)

    class Meta:
        model = Follow
        fields = ('id', 'author', 'follower')
        read_only_fields = ('author', 'follower')

    def create(self, validated_data):
        if Follow.objects.filter(author=validated_data['author'],
                                 follower=validated_data['follower']).exists():
            raise serializers.ValidationError({'author': 'Already following'})
        return super().create(validated_data)
