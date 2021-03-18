from django.contrib import admin
from .models import Order, OrderItem

# admin.site.register(Order)
# admin.site.register(OrderItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address',
                    'postal_code', 'city', 'paid', 'created']
    list_filter = ['paid', 'created',]
    inlines = [OrderItemInline]