from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import serializers
from order.models import Order, Billing
from price.models import Price

class OrderSerializer(serializers.Serializer):
    productType = serializers.IntegerField()
    selectedTheme = serializers.IntegerField()
    tires = serializers.IntegerField()

    card_name = serializers.CharField()
    card_number = serializers.CharField()
    cvv = serializers.IntegerField()
    expiry_date = serializers.CharField()
    

    def save(self, user):
        order = Order()
        order.user = user
        order.product_type = self.validated_data['productType']
        order.selected_theme = self.validated_data['selectedTheme']
        order.tires = self.validated_data['tires']
        price = get_object_or_404(Price, pk = order.product_type)
        order.price = int(price.price * order.tires * 100)
        order.status = 0
        order.save()

        billing = Billing()
        billing.order = order
        billing.card_name = self.validated_data['card_name']
        billing.card_number = self.validated_data['card_number']
        billing.cvv = self.validated_data['cvv']
        billing.expiry_date = self.validated_data['expiry_date']
        billing.save()
        return order
