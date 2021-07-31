from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse_lazy, reverse
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, EmailVerifySerializer, LoginSerializer, LogoutSerializer, ResetPasswordSerializer, ResetPasswordValidateSerializer, PasswordChangeSerializer
from .models import User
from .helper import send_email
from os import environ
from jwt import decode, ExpiredSignatureError, DecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user_object = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user_object).access_token
        
        endpoint_verified = reverse_lazy('email_verify')
        
        #http://127.0.0.1:8001
        url= f'{environ.get("URL_EMAIL")}{endpoint_verified}?token={token}'
        
        data = {
            'subject': 'Confirmar Usuario',
            'body': f'Hola {user_object.username}, usa este link para activar tu cuenta {url}',
            'to': f'{user_object.email}'
        }
        send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class EmailVerifyView(views.APIView):
    serializer_class = EmailVerifySerializer

    token_params = Parameter('token', in_=IN_QUERY, description='Token Autenticación', type=TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_params])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = decode(token, environ.get('SECRET_KEY'), algorithms='HS256')

            user = User.objects.get(id=payload['user_id'])
            message = 'El usuario ya ha sido activado anteriormente'

            if not user.is_verified:
                message = 'El usuario ha sido activado'
                user.is_verified = True
                user.is_active = True
                user.save()

            return Response({
                'success': message
            }, status=status.HTTP_200_OK)

        except ExpiredSignatureError:
            return Response({
                'error': 'El token ha expirado'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except DecodeError:
            return Response({
                'error': 'Token incorrecto'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': 'Se cerro la sesión'
        }, status=status.HTTP_200_OK)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            endpoint_validate = reverse('reset_password_check', kwargs={'uidb64': uidb64, 'token': token})

            url = f'{environ.get("URL_EMAIL")}{endpoint_validate}'
            
            data = {
                'subject': 'Cambiar Contraseña',
                'body': f'Hola {user.username}, usa este link para resetear tu contraseña {url}',
                'to': user.email
            }
            send_email(data)
        return Response({
            'success': 'El correo fue enviado'
        }, status=status.HTTP_200_OK)

class ResetPasswordCheckView(generics.GenericAPIView):
    serializer_class = ResetPasswordValidateSerializer

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise Exception('El token es incorrecto')

            return Response({
                'success': 'Token correcto'
            }, status=status.HTTP_200_OK)

        except (DjangoUnicodeDecodeError, Exception):
            return Response({
                'error': 'El token es incorrecto'
            }, status=status.HTTP_401_UNAUTHORIZED)

class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': 'Se cambio la contraseña'
        }, status=status.HTTP_200_OK)
