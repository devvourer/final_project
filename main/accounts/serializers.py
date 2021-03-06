from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label='password', required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, label='password', required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'phone', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'The two password different'})
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email address must be unique'})
        del attrs['password2']
        return attrs


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name')
