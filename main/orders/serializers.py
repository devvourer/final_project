from rest_framework import serializers
from .models import Order


class OrderCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Order
        fields = ['address', 'postal_code', 'city']

    def create(self, validated_data):
        request = self.context.get('request')
        print(f'----- {self.context}')
        return Order.objects.create(user=request.user.pk, **validated_data)


    # def create(self, validated_data):
    #     request = self.context.get('request')
    #
    #     return Order.objects.create(user=request.user, **validated_data)