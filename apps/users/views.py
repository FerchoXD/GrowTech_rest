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
#importaciones para senEmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()
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

class Logout(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        user = request.user
        RefreshToken.for_user(user)
        return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK) 

class EmailSender:
    @staticmethod
    def send_email(username):
        try:
            user = User.objects.get(username=username)
            print(f"Usuario encontrado: {user.username}")
            email = user.email

            sender_email =  os.environ.get('SENDER_EMAIL') # Cambia esto con tu dirección de correo electrónico
            receiver_email = os.environ.get('RECEIVER_EMAIL')
            password = os.environ.get('PASSWORD_EMAIL')  # Cambia esto con tu contraseña de correo electrónico

            subject = "Solicitud de ayuda y soporte"
            body = f"Se necesita ayuda y soporte para el usuario {username} con email: {email}  "

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, password)
                    server.send_message(message)
                    return True
            except smtplib.SMTPException:
                return False
        except User.DoesNotExist:
            return False

class EmailSenderView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')

        if EmailSender.send_email(username):
            return Response({
                'message': 'Ayuda y soporte se contactará contigo en seguida'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'usuario no encontrado o fallo en el servidor'
            }, status=status.HTTP_404_NOT_FOUND)