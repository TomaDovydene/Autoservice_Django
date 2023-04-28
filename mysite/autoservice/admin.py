from django.contrib import admin
from . import models

class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date', 'status']
    inlines = [OrderLineInline]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['owner_name', 'vehicle_model', 'plate', 'vin']
    list_filter = ['owner_name', 'vehicle_model__make', 'vehicle_model__model']
    search_fields = ['plate', 'vin']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity']

# Register your models here.
admin.site.register(models.VehicleModel)
admin.site.register(models.Vehicle, VehicleAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.Service, ServiceAdmin)
