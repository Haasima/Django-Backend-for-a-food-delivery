from rest_framework import viewsets
from .serializers import (ProductSerializer, 
                          OrderProductSerializer, 
                          DeliveryCourierSerializer, DeliveryCustomerSerializer)
from .models import Product, Shop, OrderProduct
from django.db.models import Prefetch
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import mixins
from .permissions import IsAdminOrCourier, IsAdminOrCustomer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []
    queryset = Product.objects.prefetch_related(Prefetch('shop', queryset=Shop.objects.select_related('address')))\
                               .select_related('category')
                               
                               
class OrderProductViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = (IsAdminUser,)
    queryset = OrderProduct.objects.select_related('customer', 'courier').prefetch_related(Prefetch('product',
                                    queryset=Product.objects.select_related('category')\
                                    .prefetch_related(Prefetch('shop', queryset=Shop.objects.select_related('address')))))
    
    
class CourierDeliveryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = DeliveryCourierSerializer
    permission_classes = (IsAdminOrCourier,)
    queryset = OrderProduct.objects.select_related("customer").only(
                        "customer__first_name", "customer__last_name", "customer__phone", "created", "delivered_at"
                        )
    
    
class CustomerDeliveryViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = DeliveryCustomerSerializer
    permission_classes = (IsAdminOrCustomer,)
    queryset = OrderProduct.objects.select_related("courier").only(
                        "courier__first_name", "courier__last_name", "courier__phone", "created", "delivered_at"
                        )