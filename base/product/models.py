from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from address.models import ShopAddress
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from address.models import UserAddress

User = get_user_model()

def product_upload_path(instance, filename):
    return f"product/{instance.product.category}/{instance.product.created}/{filename}"

class Shop(models.Model):   
    name = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True, 
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    address = models.ForeignKey(ShopAddress, related_name="shop", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name="sellers", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.shop.name}"
    
class Category(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey("self", null=True, blank=True,
                               on_delete=models.CASCADE, related_name="subcategories")
    
    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    class Status(models.TextChoices):
        OUT_OF_STOCK = "OUT OF STOCK", "Out of stock"
        IN_STOCK = "IN STOCK", "In stock"
    
    shop = models.ManyToManyField(Shop, related_name="products")
    seller = models.ForeignKey(Seller, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0)])
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0.0,
                                   validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True, 
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.OUT_OF_STOCK)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        self.price = self.price * (1 - self.discount)
        
        if self.quantity == 0:
            self.status = self.Status.OUT_OF_STOCK
        elif self.status == self.Status.OUT_OF_STOCK and self.quantity > 0:
            self.status = self.Status.IN_STOCK
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.name}"

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="photo")
    image = models.ImageField(upload_to=product_upload_path)
    
    def __str__(self):
        return f"{self.product.name}/{self.image}"

    
class OrderProduct(models.Model):
    class Status(models.TextChoices):
        SHIPPED = "SHIPPED", "Shipped"
        PROCESSING = "PROCESSING", "Processing"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELED = "CANCELED", "Canceled"
        
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_products")
    customer_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0)])
    order_quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    courier = models.ForeignKey(User, related_name="couriers", on_delete=models.SET_NULL,
                                null=True, limit_choices_to={"role": "COURIER"})
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SHIPPED)
    created = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    
    def clean(self) -> None:
        if self.product.quantity < 0:
            raise ValidationError(f"Product quantity cannot be negative.")

        if self.courier and self.courier.role != "COURIER":
            raise ValidationError("The assigned courier must have the role 'COURIER'.")
        

    def save(self, *args, **kwargs):
        # вызов clean для проверки валидаций
        self.clean()
        
        order_quantity = self.order_quantity

        # уменьшение количества товара при заказе или возвращение товара на склад
        if self._state.adding:
            if self.product.quantity < 1:
                raise ValidationError("Not enough quantity in stock.")
            self.product.quantity -= order_quantity
        else:
            if self.status == "CANCELED" and self.delivered_at is None:
                self.product.quantity += order_quantity
                order_quantity = 0 # сброс количества заказов при отмене заказа
        
        # установка времени доставки
        if self.status == "DELIVERED" and self.delivered_at is None:
            self.delivered_at = timezone.now()
            
        # price с учётом скидки и количества заказов
        self.price = self.product.price * order_quantity
            
        super().save(*args, **kwargs)
        self.product.save()
        
        
    def __str__(self):
        return f"Customer: {self.customer} | Courier: {self.courier} | Product: {self.product}"