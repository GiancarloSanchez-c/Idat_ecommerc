from django.contrib import admin
from .models import Cupon,Carrito, Venta,Detalle_Venta
# Register your models here.

@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ['codigo_cupon','descuento','fecha_fin', 'en_uso']
    
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id','programa','cantidad','precio','usuario','created_at','updated_at']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id','date_of_sale','postulante','codigo','cantidad','cupon','precio']

@admin.register(Detalle_Venta)
class DetalleVenta(admin.ModelAdmin):
    list_display = ['id','cantidad','venta','programa','precio','created_at','updated_at']
