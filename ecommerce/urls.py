from django.urls import path, include
from rest_framework import routers
from .views import HomeView,AddCarritoComprasView,CantidadUpgradeView, CantidadDowngradeView, PagoCheckout,OrderView, DetalleOrdenView,CheckoutView,ConfirmationAPIVIEW

router = routers.DefaultRouter()

router.register('carrito/agregar', AddCarritoComprasView, basename="agregar_carrito"),

router.register('cantidad/up', CantidadUpgradeView, basename="cantidad_up"),
router.register('cantidad/down', CantidadDowngradeView, basename="cantidad_down"),

router.register('pago', PagoCheckout, basename="pago"),

router.register('orden', OrderView, basename="orden"),
router.register('orden/detalle', DetalleOrdenView, basename="detalle_orden"),

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('confirmation', ConfirmationAPIVIEW.as_view(), name='confirmation'),
]
urlpatterns += router.urls