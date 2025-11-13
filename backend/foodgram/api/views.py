from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model

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
