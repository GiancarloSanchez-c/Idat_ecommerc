from django.urls import path
from .views import CursoViewSet, HorarioCursoViewSet, DetalleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('curso',CursoViewSet, basename='curso'),
router.register('horario',HorarioCursoViewSet, basename='horario'),
router.register('estudiar',DetalleViewSet, basename='estudiar'),


urlpatterns = router.urls