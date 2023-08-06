
from django.contrib import admin

from warehouses.models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']
    search_fields = ['name']
