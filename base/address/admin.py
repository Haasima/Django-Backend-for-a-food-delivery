from django.contrib import admin
from .models import UserAddress, Country, City, ShopAddress
from cities_light.models import (City as OriginalCity,
                                 Country as OriginalCountry,
                                 Region as OriginalRegion, SubRegion)


admin.site.unregister(OriginalCity)
admin.site.unregister(OriginalCountry)
admin.site.unregister(OriginalRegion)
admin.site.unregister(SubRegion)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(UserAddress)
admin.site.register(ShopAddress)