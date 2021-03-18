from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .cart import Cart
# from .serializer import CartAddProductSerializer
from shop.forms import CartAddProductForm
from shop.models import Product


@api_view(['POST'])
def cart_add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    # serializer = CartAddProductSerializer(data=request.POST)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def cart_detail(request):
    cart = Cart(request)
    print(type(cart))
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                    'update': True})
    data = {'cart': cart}
    return Response(data, template_name='cart/cart_detail.html')

