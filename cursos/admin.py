from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Horario, Curso, Detalle
# Register your models here.

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image','price','description_study','description_plan_study','status']
    ordering = ['id']

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['id','days','hours']
    ordering = ['id']
    
@admin.register(Detalle)
class DetalleAdmin(admin.ModelAdmin):
    list_display = ['id','detalle']
    ordering = ['id']
