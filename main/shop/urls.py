from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('create_category/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/', ProductListView.as_view(), name='product_list'),
    path('filtered/<int:pk>/', ProductListFilteredView.as_view(), name='product_list_filter'),
    path('create_product/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('search/', search, name='search'),
    # commentary urls
    path('commentary/create', CommentaryCreateView.as_view(), name='commentary_create'),

]