from django.db import models
from django.contrib.auth.models import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, telefono, programa):
        if username is None:
            raise TypeError('El usuario no se ha ingresado')

        if email is None:
            raise TypeError('El correo no se ha ingresado')

        user = self.model(username=username, email=self.normalize_email(email),programa=programa, telefono=telefono)
        user.save()
        return user

class InfoUser(models.Model):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    telefono = models.IntegerField()
    programa = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        jwt_token = RefreshToken.for_user(self)
        return {
            'refresh': str(jwt_token),
            'access': str(jwt_token.access_token),
        }

