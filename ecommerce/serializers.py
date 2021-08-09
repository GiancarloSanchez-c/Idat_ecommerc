from .models import Cupon, Venta, Detalle_Venta, Carrito
from rest_framework import serializers
from cursos.serializers import CursoSerializer
from cursos.models import Curso
from info_User.serializers import UserSerializer
from info_User.models import InfoUser
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
    postulante = UserSerializer(read_only=True)
    postulante_id = serializers.PrimaryKeyRelatedField(queryset=InfoUser.objects.all(), source='postulante')
    class Meta:
        model = Venta
        fields = ['id','postulante','postulante_id','codigo','precio','cupon_id','cupon']

class DetalleVentaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer(read_only=True)
    venta_id = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all(), source='venta')
    programa = CursoSerializer(read_only=True)
    programa_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='programa')
    class Meta:
        model = Detalle_Venta
        fields = ['id','cantidad','venta_id','curso_id','precio']
        