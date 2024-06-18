from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        COURIER = "COURIER", "Courier"
        CLIENT = "CLIENT", "Client"
        
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    
    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"username": self.username})