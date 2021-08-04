from .models import Curso, Horario,  Detalle
from rest_framework import serializers, status
from rest_framework import viewsets
from .serializers import CursoSerializer, HorarioSerializer, DetalleSerializer
from rest_framework.response import Response
# Create your views here.
class CursoViewSet(viewsets.ModelViewSet):
    serializer_class = CursoSerializer
    look_field= 'id'
    queryset = Curso.objects.all()
        
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = request.data
        serializer = self.serializer_class(data=serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': 'Curso creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        serializer = self.queryset().filter(id=pk).first()
        if serializer:
            serializer.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'error': 'No existe ninguna información'
        }, status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe ninguna información'},status=status.HTTP_400_BAD_REQUEST)

class HorarioCursoViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioSerializer
    look_field= 'id'
    queryset = Horario.objects.all()    

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = request.data
        serializer = self.serializer_class(data=serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': 'Horario creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        serializer = self.queryset().filter(id=pk).first()
        if serializer:
            serializer.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'error': 'No existe ninguna información'
        }, status = status.HTTP_400_BAD_REQUEST)

class DetalleViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleSerializer
    look_field= 'id'
    queryset = Detalle.objects.all()    

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = request.data
        serializer = self.serializer_class(data=serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': 'Creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        serializer = self.queryset().filter(id=pk).first()
        if serializer:
            serializer.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'error': 'No existe ninguna información'
        }, status = status.HTTP_400_BAD_REQUEST)
