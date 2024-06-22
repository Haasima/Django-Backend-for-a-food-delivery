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
    seller = SellerSerializer()
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'quantity', 'description',
            'discount', 'price', 'status', 'rate',
            'created', 'seller'
        )
    
    def create(self, validated_data):
        seller_data = validated_data.get('seller')
        seller_shop_data = seller_data.get('shop').pk
        seller_user_data = seller_data.get('user').pk
        
        user = User.objects.filter(id=seller_user_data).first()
        shop = Shop.objects.filter(id=seller_shop_data).first()
        
        seller = Seller.objects.filter(user=user, shop=shop).first()

        product = Product.objects.create(seller=seller, **validated_data)
        product.shop.set([shop])
        return product
    
    def update(self, instance, validated_data):
        seller_data = validated_data.get('seller', None)
        shop_data = validated_data.get('shop', None)

        if seller_data:
            seller_shop_data = seller_data.get('shop').pk
            seller_user_data = seller_data.get('user').pk

            user = User.objects.filter(id=seller_user_data).first()
            shop = Shop.objects.filter(id=seller_shop_data).first()

            seller = Seller.objects.filter(user=user, shop=shop).first()
            
            if seller is None:
                raise serializers.ValidationError("The specified seller does not exist.")

            instance.seller = seller

        if shop_data:
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

    class Meta:
        model = OrderProduct
        fields = (
                'id', 'status', 'created', 'delivered_at', 'customer', 'courier',
                'product',
                )
        
    def create(self, validated_data):
        customer = validated_data.get('customer')
        product = validated_data.get('product')
        
        customer_address = UserAddress.objects.filter(user=customer).first()
        if not customer_address:
            raise serializers.ValidationError("The customer does not have a valid address.")
        
        # Создание объекта OrderProduct с указанием всех необходимых полей
        order_product = OrderProduct(
            customer=customer,
            customer_address=customer_address,
            courier=validated_data.get('courier'),
            product=product,
            price=product.price,
            status=validated_data.get('status', 'SHIPPED')
        )
        
        order_product.save()
        
        return order_product

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