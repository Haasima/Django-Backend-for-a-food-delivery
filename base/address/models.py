from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from cities_light.abstract_models import AbstractCity, AbstractCountry
from cities_light.receivers import connect_default_signals
from cities_light.settings import CITIES_LIGHT_APP_NAME
from django.contrib.auth import get_user_model

User = get_user_model()

class Country(AbstractCountry):
    pass

connect_default_signals(Country)

class City(AbstractCity):
    timezone = models.CharField(max_length=40)
    subregion = models.ForeignKey(CITIES_LIGHT_APP_NAME + '.SubRegion',
                                  blank=True, null=True,
                                  on_delete=models.CASCADE, related_name="subregions")
    region = models.ForeignKey(CITIES_LIGHT_APP_NAME + '.Region', blank=True,
                               null=True, on_delete=models.CASCADE, related_name="regions")
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE, related_name="countries")
connect_default_signals(City)

class BaseAddress(models.Model):
    class HouseType(models.TextChoices):
        RESIDENTIAL_BUILDING = "RESIDENTIAL BUILDING", "Residential building"
        LANDED_HOUSE = "LANDED HOUSE", "Landed house"
        
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country")
    city = ChainedForeignKey(City, chained_field="country", chained_model_field="country", related_name="city")
    street = models.CharField(max_length=100)
    building_type = models.CharField(max_length=50, choices=HouseType.choices, default=HouseType.RESIDENTIAL_BUILDING)
    building_number = models.PositiveIntegerField()
    entrance_number = models.PositiveIntegerField(blank=True, null=True)
    apartment_number = models.PositiveIntegerField(blank=True, null=True)
    
    
class UserAddress(BaseAddress):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    code_number = models.CharField(max_length=8, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} — {self.city} — {self.street}"
    
class ShopAddress(BaseAddress):
    def __str__(self):
        return f"{self.city} — {self.street}" 