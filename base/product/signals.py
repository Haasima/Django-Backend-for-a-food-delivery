from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seller, Product

@receiver(post_save, sender=Product)
def set_shop(sender, instance, created, **kwargs):
    if created:
        instance.shop.add(instance.seller.shop)
        instance.save()