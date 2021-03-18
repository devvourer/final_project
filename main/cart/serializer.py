from rest_framework import serializers
from shop.models import Product

# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
#
#
# class CartAddProductSerializer(serializers.ModelSerializer):
#     quantity = serializers.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
#     update = serializers.BooleanField(required=False, initial=False)
#
#     class Meta:
#
#         fields = ['quantity', 'update']


