from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(max_length=60, min_length=6, write_only=True)    
    default_error_messages = {
        'username':'El usuario debe de contener caracteres alfanuméricos'
    }
    class Meta:
        model = User
        fields = ['username', 'email','password']
        
    def validate(self, attrs):
        username = attrs.get('username', '')
        if username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return user.tokens()

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        if not email:
            raise serializers.ValidationError('Debes ingresar un correo electrónico')

        if not password:
            raise serializers.ValidationError('Debes ingresar una contraseña')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Credenciales erroneas, vuelvalo a intentar')

        if not user.is_verified:
            raise AuthenticationFailed('Su correo no esta verificado')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token Expirado o incorrecto'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
            
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3)
              
class ResetPasswordValidateSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=6, write_only=True)

class PasswordChangeSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            confirm_password = attrs.get('confirm_password', '')
            token = attrs.get('token', '')
            uidb64 = attrs.get('uidb64', '')

            if password != confirm_password:
                raise AuthenticationFailed('Las contreñas no son iguales')

            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El token no es válido')

            user.set_password(password)
            user.save()

            return True
        except (DjangoUnicodeDecodeError, Exception):
            raise AuthenticationFailed('Los datos no son correctos')
