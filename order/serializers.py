from rest_framework import serializers

from order.models import Order, Billing


class OrderSerializer(serializers.Serializer):
    productType = serializers.IntegerField()
    selectedTheme = serializers.IntegerField()
    tires = serializers.IntegerField()
    price = serializers.FloatField()

    card_name = serializers.CharField()
    card_number = serializers.CharField()
    cvv = serializers.IntegerField()
    price = serializers.FloatField()
    expiry_date = serializers.CharField()
    transaction_code = serializers.CharField()

    def save(self, user):
        order = Order()
        order.user = user
        order.product_type = self.validated_data['productType']
        order.selected_theme = self.validated_data['selectedTheme']
        order.tires = self.validated_data['tires']
        order.price = self.validated_data['price']
        order.status = 0
        order.save()

        billing = Billing()
        billing.order = order
        billing.card_name = self.validated_data['card_name']
        billing.card_number = self.validated_data['card_number']
        billing.cvv = self.validated_data['cvv']
        billing.price = self.validated_data['price']
        billing.expiry_date = self.validated_data['expiry_date']
        billing.transaction_code = self.validated_data['transaction_code']
        billing.save()
        return order
