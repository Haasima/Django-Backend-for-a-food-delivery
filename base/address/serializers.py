from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserAddress, Country, City

User = get_user_model()

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)
        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)

class UserAddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()
    
    class Meta:
        model = UserAddress
        fields = ('country', 'city',
                  'street', 'building_type',
                  'building_number', 'entrance_number',
                  'code_number', 'apartment_number')