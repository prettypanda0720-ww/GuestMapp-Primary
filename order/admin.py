from django.contrib import admin
from .models import Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)