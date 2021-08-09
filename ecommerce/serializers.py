from .models import Cupon, Venta, Detalle_Venta, Carrito
from authentication.models import User
from rest_framework import serializers
from cursos.serializers import CursoSerializer
from cursos.models import Curso

class AddCarritoComprasSerializer(serializers.ModelSerializer):
    programa=CursoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso') 
    class Meta:
        model = Carrito
        fields = ['id','programa','cantidad','precio','programa_id']
    
class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'
class UpgradeSerializer(serializers.ModelSerializer):
    up = serializers.IntegerField(default=1)
    class Meta:
        model = Carrito
        fields = ['up']
class DowngradeSerializer(serializers.ModelSerializer):
    down = serializers.IntegerField(default=1)
    class Meta:
        model = Carrito
        fields = ['down']
class VentaSerializer(serializers.ModelSerializer):
    cupon = CuponSerializer(read_only=True)
    cupon_id = serializers.PrimaryKeyRelatedField(queryset=Cupon.objects.all(), source='cupon')
    postulante = User(read_only=True)
    postulante_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='postulante')
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer(read_only=True)
    venta_id = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all(), source='venta')
    programa = CursoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='programa')
    class Meta:
        model = Detalle_Venta
        fields = '__all__'
        

