from django.contrib.auth import authenticate
from rest_framework.authentication import BaseAuthentication
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from apps.users.api.serializers import (
    CustomTokenObtainPairSerializer, CustomUserSerializer, UserRegisterSerializer,LogoutSerializer
)
from apps.users.models import User



class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                user_id = user.id
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'user_id': user_id, 
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None

class Register(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        account = serializer.save()
        
        data = {
            'response': 'Cuenta creada correctamente',
            'username': account.username,
            'email': account.email,
            'password': account.password
        }
        
        return Response(data, status=status.HTTP_201_CREATED)

'''
class Logout(GenericAPIView):

    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 1))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)
'''
class Logout(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        user = request.user
        RefreshToken.for_user(user)
        return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)