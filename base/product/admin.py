from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Shop, Product, ProductImage, Category, OrderProduct, Seller
from django.db.models import Prefetch


@admin.register(Seller)
class SellerModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop')
    list_filter = ('shop',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderProduct._meta.get_fields()]
    list_filter = ('status', 'created', 'delivered_at')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        return qs.prefetch_related(Prefetch('parent', queryset=Category.objects.select_related('parent')))
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_shops', 'category', 'name', 'status', 'price')
    list_filter = ('category', 'status')
    
    def get_shops(self, obj):
        return ", ".join([shop.name for shop in obj.shop.all()])
    get_shops.short_description = 'Shops'
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        return qs.select_related('category').prefetch_related('shop')

admin.site.register(ProductImage)