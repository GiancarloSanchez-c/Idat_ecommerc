from django.shortcuts import render
from cursos.models import Curso,Venta,Detalle_Venta
from cursos.serializers import CursoSerializer, DetalleVentaSerializer
from .models import Carrito
from rest_framework.generics import ListAPIView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import F
from rest_framework.viewsets import  ViewSet
from rest_framework.permissions import IsAuthenticated 
from json import loads
from .utils import random_code
from django.http.response import JsonResponse
from .paypal import Order
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class HomeView(ListAPIView):
    model = Curso
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def get_context_data(self, **kwargs):
        carrito = Carrito.objects.filter(user=self.request.user).count()
        print(carrito)
        context = super().get_context_data(**kwargs)
        print(context)
        context['checkout'] = carrito
        return context
    
class CheckoutView(ListAPIView): 

    def get_queryset(self):
        return Carrito.objects.filter(user=self.request.usuario).order_by('created_at')
    
class ConfirmationAPIVIEW(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'confirmation.html'

    def get(self, request):
        queryset = Venta.objects.all()
        return Response({'confirmation': queryset})
    
    
class AddCarritoComprasView(ViewSet):
    def create(self, request, *args, **kwargs):
        body = request.POST
        curso_id = body['curso_id'] # Trae el id del curso
        product_query = Curso.objects.get(id=curso_id)
        if product_query:
            price = product_query.price
            try:
                carrito = Carrito.objects.get(curso_id=curso_id, user=request.user) #Trae el curso detallado
                messages.add_message(request, messages.ERROR, 'El producto ya se encuentra agregado')
            except Carrito.DoesNotExist:
                carrito = Carrito(curso_id=curso_id, price=price, quantity=1, user=request.user)
                carrito.save()
                messages.add_message(request, messages.SUCCESS, 'El producto se agrego al carrito')
        return redirect(reverse_lazy('index')) # Redirecciona al menu
    
class CantidadUpgradeView(ViewSet):
    def create(self, request, *args, **kwargs):
        carrito = Carrito.objects.get(pk=kwargs['pk'])
        if carrito:
            carrito.quantity = F('cantidad') + 1
            carrito.save()
        return redirect(reverse_lazy('checkout'))
    
class QuantityDowngradeView(ViewSet):
    def post(self, request, *args, **kwargs):
        shopping_cart = Carrito.objects.get(pk=kwargs['pk'])
        if shopping_cart:
            if shopping_cart.quantity > 1:
                shopping_cart.quantity = F('quantity') - 1
                shopping_cart.save()
            elif shopping_cart.quantity == 1:
                shopping_cart.delete()
        return redirect(reverse_lazy('checkout'))
    
class PagoCheckout(ViewSet):
    
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        order_id = body['orderID']

        carrito = Carrito.objects.filter(user=request.user).all()
        total_price = round(sum(round(d.price * d.quantity, 2) for d in carrito), 2)

        order = Order().get_order(order_id)
        order_price = float(order.result.purchase_units[0].amount.value)

        if order_price == total_price:
            return self._order_capture(
                order_id, order_price, request, carrito
            )

        return JsonResponse({
            'error': 'Sucedio un error al realizar el cobro'
            
        })

    def _order_capture(self, order_id, order_price, request, carrito):
        order_capture = Order().capture_order(order_id, debug=True)

        code = f'OC-{random_code(5)}'
        order = Venta.objects.create(price=order_price, user=request.user, code=code)
        if order:
            order_id = order.pk
            for value in carrito:
                Detalle_Venta.objects.create(order_id=order_id, product_id=value.product.id, quantity=value.quantity, price=value.price)
            Carrito.objects.filter(user=request.user).delete()

        data = {
            'id': order_capture.result.id,
            'name': order_capture.result.payer.name.given_name
        }
        
        return JsonResponse(data)
    
class OrderView(ViewSet):
    def get_queryset(self):
        return Venta.objects.filter(user=self.request.user).all()

class DetalleOrdenView(ViewSet):
    def get_queryset(self):
        return Detalle_Venta.objects.filter(order__code=self.kwargs['codigo']).all()

    def get_context_data(self, **kwargs):
        order = Venta.objects.get(code=self.kwargs['codigo'])
        context = super().get_context_data(**kwargs)
        context['order'] = order
        return context 
