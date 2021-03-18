from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('', include('shop.urls')),
    path('account/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
]
