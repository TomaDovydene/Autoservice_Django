from django.contrib import admin
from . import models

class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date']

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['owner_name', 'vehicle_model', 'plate', 'vin']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

# Register your models here.
admin.site.register(models.VehicleModel)
admin.site.register(models.Vehicle, VehicleAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine)
admin.site.register(models.Service, ServiceAdmin)
