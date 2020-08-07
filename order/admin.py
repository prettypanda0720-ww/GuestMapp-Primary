from django.contrib import admin
from .models import Order, Billing, Price
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    pass

class BillingAdmin(admin.ModelAdmin):
    pass

class PriceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)
admin.site.register(Billing, BillingAdmin)
admin.site.register(Price, PriceAdmin)