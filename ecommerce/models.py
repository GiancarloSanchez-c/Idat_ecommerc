from django.db import models
from authentication.models import User
from cursos.models import Curso

# Create your models here.
class Cupon(models.Model):
    id = models.AutoField(primary_key = True)
    codigo_cupon = models.CharField(max_length= 10)
    descuento = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_fin = models.DateField()
    en_uso = models.BooleanField(default=False)
    class Meta:
        db_table = 'cupon'
        verbose_name = 'Cupon'
        verbose_name_plural = 'Cupones'
    
    def __str__(self):
        return self.codigo_cupon
    
class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    programa = models.ForeignKey(Curso, null=True, blank=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carrito'
        verbose_name = 'Carrito de Compra'
        verbose_name_plural = 'Carrito de Compras'

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_sale = models.DateField(auto_now_add=True)
    postulante = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=200)
    cantidad = models.IntegerField(default=1)
    cupon = models.ForeignKey(Cupon, on_delete=models.SET_NULL, blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return self.id
    
class Detalle_Venta(models.Model):
    id = models.AutoField(primary_key = True)
    cantidad = models.IntegerField(default=1)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    programa = models.ForeignKey(Curso, on_delete = models.CASCADE)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'detalle_orden'
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'

    def __str__(self):
        return self.id
