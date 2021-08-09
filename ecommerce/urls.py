from django.urls import path, include
from rest_framework import routers
from .views import HomeView,AddCarritoComprasView,CantidadUpgradeView, CantidadDowngradeView, PagoCheckout,OrderView, DetalleOrdenView,CheckoutView,ConfirmationAPIVIEW

router = routers.DefaultRouter()

router.register('cantidad/up', CantidadUpgradeView, basename="cantidad_up"),
router.register('orden/detalle', DetalleOrdenView,  basename='detalle_orden'),
router.register('orden', OrderView, basename='orden'),
router.register('cantidad/down', CantidadDowngradeView, basename="cantidad_down"),
router.register('confirmation', ConfirmationAPIVIEW, basename='confirmation'),
router.register('pago', PagoCheckout, basename="pago"),

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('carrito/agregar', AddCarritoComprasView.as_view(), name="agregar_carrito"),
]
urlpatterns += router.urls