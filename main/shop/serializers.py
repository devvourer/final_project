from rest_framework import serializers
from .models import Category, Product, Commentary


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

        def create(self, validate_data):
            category = Category.objects.create(**validate_data)
            category.save()
            return category


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'id')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'image', 'image_out_source')


class ProductListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'id', 'products')


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'title', 'slug', 'price', 'image', 'image_out_source')

        def create(self, validate_data):
            product = Product.objects.create(**validate_data)
            product.save()
            return product

#
class DetailProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'image', 'id')



class CommentaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ('body', 'product', 'user')




