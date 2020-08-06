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
        (1, 'working'),
        (2, 'completed'),
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
