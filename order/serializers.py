from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.Serializer):
    productType = serializers.IntegerField()
    selectedTheme = serializers.IntegerField()
    tires = serializers.IntegerField()
    price = serializers.FloatField()
    status = serializers.IntegerField()

    def save(self, user):
        order = Order()
        order.user = user
        order.product_type = self.validated_data['productType']
        order.selected_theme = self.validated_data['selectedTheme']
        order.tires = self.validated_data['tires']
        order.price = self.validated_data['price']
        order.status = self.validated_data['status']
        order.save()
        return order
