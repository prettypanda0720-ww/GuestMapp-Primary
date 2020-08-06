from django.db import models

# Create your models here.
from order.models import Order


class Billing(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    cvv = models.IntegerField()
    price = models.FloatField()
    transaction_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'billing'
