from .models import Curso, Horario,  Detalle
from rest_framework import serializers

class HorarioSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Horario 
        fields = ['id','days','hours']
        
class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle 
        fields = ['id','detalle']   
class CursoSerializer(serializers.ModelSerializer):
    horario=HorarioSerializer()
    detalle = DetalleSerializer()
    class Meta:
        model = Curso
        fields = ['id','title','image','description_study','horario','detalle','description_plan_study','price','status']