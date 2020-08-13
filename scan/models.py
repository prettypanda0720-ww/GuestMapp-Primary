from django.db import models

# Create your models here.
from backend import settings
from order.models import Order


class ScanTable(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    scanImageRaw = models.ImageField(upload_to='scan/%Y/%m/%d', blank=True, null=True)
    scanImageUrl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "scan_table"

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order.id,
            'title': self.title,
            'scanImageRaw': settings.BASE_URL + self.scanImageRaw if self.scanImageRaw else None,
            'scanImageUrl': self.scanImageUrl
        }


class ScanDetailsTable(models.Model):
    scan = models.ForeignKey(ScanTable, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=255)
    scanDetailImageRaw = models.ImageField(
        blank=True,
        null=True,
        upload_to='scan/',
    )
    scanDetailImageUrl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "scan_details_table"

    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan.id,
            'title': self.title,
            'scanDetailImageRaw': settings.BASE_URL + self.scanDetailImageRaw.url if self.scanDetailImageRaw else None,
            'scanDetailImageUrl': self.scanDetailImageUrl
        }

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='scan/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)