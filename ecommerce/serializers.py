from .models import Cupon, Venta, Detalle_Venta, Carrito
from info_User.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email')
class AddCarritoComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'
    
class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Venta
        fields = '__all__'
        

