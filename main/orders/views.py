from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import OrderItem, Order
from .serializers import OrderCreateSerializer
from cart.cart import Cart
from .forms import OrderCreateForm


class OrderCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/create.html'

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return Response({'form': form, 'cart': cart})


class OrderDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/created.html'
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = OrderCreateForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            order = form.cleaned_data
            order = Order.objects.create(user=request.user, address=order['address'],
                                        postal_code=order['postal_code'], city=order['city'])
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()
            return Response({'order': order})
        else:
            return HttpResponseRedirect(redirect_to='order_create')





