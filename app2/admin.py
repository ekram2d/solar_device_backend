from django.contrib import admin
from .models import CustomUser,Devices,BrandInformation,DeviceInformation,DeviceLocation
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Devices)
admin.site.register(BrandInformation)
admin.site.register(DeviceInformation)
admin.site.register(DeviceLocation)