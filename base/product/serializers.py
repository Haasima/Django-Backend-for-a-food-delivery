from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Shop, Product, Category, OrderProduct, Seller
from address.models import UserAddress
from django.contrib.auth import get_user_model

User = get_user_model()


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__" 
        
class SellerSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Seller
        fields = ('id', 'user', 'shop',)
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        phone = user_data['phone']
        user = User.objects.filter(phone=phone).first()

        seller = Seller.objects.filter(user=user).first()
        return seller
        
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'quantity', 'description',
            'discount', 'price', 'status', 'rate',
            'created', 'seller'
        )
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
    
    def update(self, instance, validated_data):
        seller = validated_data.get('seller', None)
            
        if seller is None:
            raise serializers.ValidationError("The specified seller does not exist.")

        instance.seller = seller
        shop = seller.shop
        instance.shop.set([shop])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'phone',
        )
        
class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'phone',
        )
        
class OrderProductSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    courier = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(choices=OrderProduct.Status.choices, default=OrderProduct.Status.SHIPPED)
    order_quantity = serializers.IntegerField(default=1)
    price = serializers.DecimalField(max_digits=13, decimal_places=2, default=0.0)
    
    class Meta:
        model = OrderProduct
        fields = (
                'id', 'status', 'order_quantity', 'price', 'created', 'delivered_at',
                'customer', 'courier', 'product',
                )
        
    def create(self, validated_data):
        customer = validated_data.get('customer')
        
        customer_address = UserAddress.objects.filter(user=customer).first()
        if not customer_address:
            raise serializers.ValidationError("The customer does not have a valid address.")
        
        # Создание объекта OrderProduct с указанием всех необходимых полей
        order_product = OrderProduct(
            customer_address=customer_address,
            **validated_data
        )
        
        order_product.save()
        
        return order_product
    
    def update(self, instance, validated_data):
        product = validated_data.get('product')
        status = validated_data.get('status', 'SHIPPED')
        delivered_at = validated_data.get('delivered_at', None)
        new_order_quantity = validated_data.get('order_quantity', 0)
        current_order_quantity = instance.order_quantity

        # Рассчитываем разницу между текущим количеством заказа и новым количеством заказа
        difference_quantity = new_order_quantity - current_order_quantity

        # Проверяем, есть ли достаточно количества продукта для удовлетворения нового заказа
        if product.quantity < difference_quantity:
            raise ValidationError("Not enough quantity in stock.")
    
        # Обновляем количество продукта
        product.quantity -= difference_quantity
        
        # Если заказ отменён, то возвращаем количество продуктов
        if status == "CANCELED" and delivered_at is None:
            product.quantity += new_order_quantity
            new_order_quantity = 0
            
        product.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
        

class DeliveryCourierSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = OrderProduct
        fields = (
            'customer', 'customer_address', 'created', 'delivered_at',
        )
        
class DeliveryCustomerSerializer(serializers.ModelSerializer):
    courier = CourierSerializer()
    class Meta:
        model = OrderProduct
        fields = (
            'courier', 'created', 'delivered_at',
        )