from django.db import models
from users.models import User

class Order(models.Model):
    """
    Order Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    choices = (
        (0, 'Blueprint'),
        (1, 'Themed 3D staging'),
        (2, 'Custom interio design 3D'),
        (3, 'Custom mobile home 3D'),
    )
    product_type = models.IntegerField(default=0, choices=choices)
    selected_theme = models.IntegerField()
    tires = models.IntegerField()
    currency = models.CharField(max_length=10)
    price = models.FloatField()

    statusChoices = (
        (0, 'pending'),
        (1, 'ready'),
        (2, 'working'),
        (3, 'completed'),
        (4, 'cancelled'),
        (5, 'confirmed'),
    )
    status = models.IntegerField(default=0, choices=statusChoices)
    created_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "order"

    def __str__(self):
        return "order" + str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'productType': self.product_type,
            'selectedTheme': self.selected_theme,
            'tires': self.tires,
            'price': self.price,
            'status': self.status,
            'createdTime': self.created_date,
            'completedTime': self.completed_date,
        }

class Billing(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    cvv = models.IntegerField()
    price = models.FloatField()
    expiry_date = models.CharField(max_length=255)
    transaction_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'billing'
    
    def __str__(self):
        return "billing" + str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'card_name': self.card_name,
            'card_number': self.card_number,
            'cvv': self.cvv,
            'price': self.price,
            'expiry_date': self.expiry_date,
            'transaction_code': self.transaction_code,
        }

class Price(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    old_price = models.FloatField()
    unit = models.CharField(max_length=255)

    class Meta:
        db_table = 'price'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'old_price': self.old_price,
            'unit': self.unit,
        }