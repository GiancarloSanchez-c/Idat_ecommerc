from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.urls import reverse_lazy
from os import environ
from .models import InfoUser
from .helper import send_email
from .serializers import InfoSerializer, UserSerializer

# Create your views here.

class RegisterInfoView(generics.GenericAPIView):
    serializer_class = InfoSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user_object = InfoUser.objects.get(email=user_data['email'])
        #token = RefreshToken.for_user(user_object).access_token
        
        endpoint_verified = reverse_lazy('info')
        
        #http://127.0.0.1:8001
        url= f'{environ.get("URL_EMAIL")}{endpoint_verified}?token={"token"}'
        
        data = {
            'subject': 'Registro de Programa',
            'body': f'''Bienvenido {user_object.username}, Gracias por postular al programa, has obtenido un 10% en tu primera compra de tu primer curso. Ingresa a nuestra página web para ver mas detalles del curso''',
            'to': f'{user_object.email}'
        }
        send_email(data)
        return Response({
            'success': 'Postulación registrada con éxito'
        }, status=status.HTTP_201_CREATED)
    
class UserListView(ListAPIView):
    queryset = InfoUser.objects.all()
    serializer_class = UserSerializer
    