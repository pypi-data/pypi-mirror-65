from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, UserWithDetailSerializer, UserLoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('groups').all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def add_permission(self, request, pk=None):
        from .services import user_add_permission
        permission_id = int(request.POST.get('permission_id'))
        user = user_add_permission(
            permission_id=permission_id,
            user_id=pk
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_group(self, request, pk=None):
        id_group = int(request.POST.get('id_group'))
        from .services import user_add_group
        user = user_add_group(
            grupo_id=id_group,
            user_id=pk
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        from .services import user_change_password
        password_old = request.POST.get('password_old')
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')
        user_change_password(
            user_id=pk,
            password_new=password,
            password_new_confirmation=password_2,
            password_old=password_old
        )
        return Response({'result': 'La contraseña se ha cambiado correctamente'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def validate_new_username(self, request) -> Response:
        validacion_reponse = {}
        from .services import user_exist_username
        username = self.request.GET.get('username', None)
        if user_exist_username(username=username):
            raise serializers.ValidationError({'username': 'Ya exite'})
        return Response(validacion_reponse)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def validate_username_login(self, request) -> Response:
        from .services import user_exist_username
        validacion_reponse = {}
        username = self.request.GET.get('username', None)
        if not user_exist_username(username=username):
            raise serializers.ValidationError({'username': 'Este usuario no existe'})
        return Response(validacion_reponse)


class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request) -> Response:
        from .services import user_get_token
        serializer = self.get_serializer(data=self.request.POST)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = user_get_token(user_id=user.id)
        return Response({
            "user": UserWithDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny, ])
    def load_user(self, request) -> Response:
        if self.request.user.is_anonymous:
            serializer = UserWithDetailSerializer(None, context={'request': request})
            return Response(serializer.data)
        serializer = UserWithDetailSerializer(self.request.user, context={'request': request})
        return Response(serializer.data)
