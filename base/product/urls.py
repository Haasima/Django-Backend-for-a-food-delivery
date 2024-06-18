from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'product'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderProductViewSet)
router.register(r'delivery/courier', views.CourierDeliveryViewSet, basename="delivery_courier")
router.register(r'delivery/customer', views.CustomerDeliveryViewset, basename="delivery_customer")

urlpatterns = [
    path('', include(router.urls)),
]
