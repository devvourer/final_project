from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http.response import *
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from .serializers import *
from rest_framework import generics, status
from .pagination import ListPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .parser import *
from .models import Product, Category, Commentary
# from cart.serializer import CartAddProductSerializer
from .forms import CartAddProductForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class CategoryListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category_list.html'


    def get(self, request):
        queryset = Category.objects.all()
        return Response({'categories': queryset})



class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CreateCategorySerializer



class ProductListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category_products_list.html'

    def get(self, request, pk):
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if pk:
            category = Category.objects.get(pk=pk)
            products = products.filter(category=category)
            paginator = Paginator(products, 5)
            page = request.GET.get('page')
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
            return Response({'products': products, 'category': category, 'page': page})



class ProductListFilteredView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category_products_list.html'

    def get(self, request, pk):
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        products = products.order_by('-price')
        if pk:
            category = Category.objects.get(pk=pk)
            products = products.filter(category=category)
            paginator = Paginator(products, 5)
            page = request.GET.get('page')
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
            return Response({'products': products, 'category': category, 'page': page})


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product_detail.html'
    pagination_class = ListPagination


    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = CartAddProductForm()
        commentary = Commentary.objects.filter(product=pk)
        return Response({'commentary': commentary, 'form': form, 'product': product})



@api_view(['POST', 'GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def search(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                products = Product.objects.filter(title__icontains=cd['query'])
                return Response({'form': form, 'products': products}, template_name='search.html')

            except ObjectDoesNotExist:
                return HttpResponse('product not found :(')
    else:
        form = SearchForm()
    return Response({'form': form}, template_name='search.html')


class CommentaryCreateView(generics.CreateAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentaryCreateSerializer
    permission_classes = [IsAuthenticated]




# create model functions
# monitors = Category.objects.get(name='monitors')
# stone = Category.objects.get(name='stone')
# gpu = Category.objects.get(name='GPU')
# memory = Category.objects.get(name='memory')
# motherboard = Category.objects.get(name='motherboard')
#
#
# def parser(request, url, category):
#     if request.method == 'GET':
#         products = get_page_data(get_html(url))
#         for i in products:
#             product = Product(title=i[0], price=i[1], image_out_source=i[2], category=category)
#             product.save()
#
#         return Response({'ok'}, status=status.HTTP_200_OK)
#     return Response({"OK"}, status=status.HTTP_226_IM_USED)