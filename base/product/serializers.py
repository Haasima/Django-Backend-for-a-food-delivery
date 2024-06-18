from rest_framework import serializers
from .models import Shop, Product, Category, OrderProduct
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        exclude = ('description',)
        
        
class ProductSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = (
            'id', 'name',
            'category', 'status', 'rate',
            'created', 'shop'
        )
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'phone',
        )
        
class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'phone',
        )
        
class OrderProductSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    courier = CourierSerializer()
    product = ProductSerializer()
    class Meta:
        model = OrderProduct
        fields = (
                'id', 'status', 'created', 'delivered_at', 'customer', 'courier',
                'product',
                )
        
class DeliveryCourierSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = OrderProduct
        fields = (
            'customer', 'created', 'delivered_at',
        )
        
class DeliveryCustomerSerializer(serializers.ModelSerializer):
    courier = CourierSerializer()
    class Meta:
        model = OrderProduct
        fields = (
            'courier', 'created', 'delivered_at',
        )