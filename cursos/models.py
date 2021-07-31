from django.db import models

# Create your models here.
class Detalle(models.Model):
    id = models.AutoField(primary_key=True)
    detalle = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'detalle'
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'

    def __str__(self):
        return self.detalle
    
class Horario(models.Model):
    id = models.AutoField(primary_key=True)
    days = models.CharField(max_length=200)
    hours = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'horario'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return f'{self.days}, {self.hours}'
    
class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField()
    description_study = models.TextField()
    horario = models.ForeignKey(Horario, null=True, on_delete=models.CASCADE)
    detalle = models.ForeignKey(Detalle, null=True, on_delete=models.CASCADE)
    description_plan_study = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'curso'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return f'{self.title} : {self.price}'
