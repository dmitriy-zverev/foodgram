from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model

from djoser.serializers import SetPasswordSerializer

from users.serializers import UserSerializer, UserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method.lower() == 'get':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserCreateSerializer(request.user,
                                          data=request.data,
                                          partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False,
            methods=['post'],
            url_path='set_password',
            permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']

        user = request.user
        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
