# Create your views here.
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.decorators import login_required
from order.models import Order
from scan.models import ScanTable, ScanDetailsTable, Photo
from scan.serializers import ScanTableSerializer, ScanDetailsTableSerializer
from .forms import PhotoForm
from backend import settings
import time

class ScanTableApiViewSet(ModelViewSet):
    """
    Scan table get/update api
    """

    http_method_names = ['get', 'post']
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ScanTableSerializer

    def get_queryset(self):
        order_id = self.request.data['order_id']
        return ScanTable.objects.filter(order=order_id).first()

    def list(self, request, *args, **kwargs):
        scan = self.get_queryset()
        if scan:
            return JsonResponse({
                'success': True,
                'message': 'success to get scan table',
                'errCode': -1,
                'data': scan.to_dict()
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'success': False,
            'message': 'scan table is not exist',
            'errCode': 0,
            'data': None
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scan = serializer.save(user=request.user)
        return JsonResponse({
            'success': True,
            'message': 'success to create scan table',
            'errCode': -1,
            'data': scan.to_dict()
        }, status=status.HTTP_200_OK)


class ScanDetailsTableApiViewSet(ModelViewSet):
    """
    Scan table get/update api
    """

    http_method_names = ['get', 'post']
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ScanDetailsTableSerializer

    def get_queryset(self):
        order_id = self.request.GET['order_id']
        try:
            scan = ScanTable.objects.filter(order_id=order_id).last()
            return ScanDetailsTable.objects.filter(scan=scan.id)
        except:
            return None

    def list(self, request, *args, **kwargs):
        scanDetails = self.get_queryset()
        if scanDetails:
            return JsonResponse({
                'success': True,
                'message': 'success to get scan detail table list',
                'errCode': -1,
                'data': [scanDetail.to_dict() for scanDetail in scanDetails]
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'success': False,
            'message': 'scan detail is not exist',
            'errCode': 0,
            'data': None
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scan = serializer.save(user=request.user)
        return JsonResponse({
            'success': True,
            'message': 'success to create scan detail table',
            'errCode': -1,
            'data': scan.to_dict()
        }, status=status.HTTP_200_OK)

    def remove(self, request, *args, **kwargs):
        try:
            scan_detail_id = request.POST.get('scan_detail_id')
            scanDetail = ScanDetailsTable.objects.get(id=scan_detail_id)
        except:
            return JsonResponse({
                'success': False,
                'message': 'Scan detail is not exist',
                'errCode': -1,
                'data': None
            })
        scanDetail.delete()
        return JsonResponse({
            'success': True,
            'message': 'success to remove scan detail ',
            'errCode': 0,
            'data': None
        })

@login_required
def ProgressBarUpload(request):
    time.sleep(1)

    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
        photo = form.save()
        photo.title = photo.file.url
        photo.save()
        data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)

@login_required
def uploadscan(request):
    data = {'success': False, 'message': None}
    if request.method == 'POST':
        rawImageUrl = request.POST.get('rawImageUrl', '').strip()
        orderid = request.POST.get('orderid', '').strip()
        airbnb = request.POST.get('airbnb', '').strip()
        google_drive = request.POST.get('google_drive', '').strip()
        if rawImageUrl:
            imageUrl = rawImageUrl
        elif airbnb:
            imageUrl = airbnb
        elif google_drive:
            imageUrl = google_drive
        else:
            data = {'success': False, 'message': None}

        scan, created = ScanTable.objects.get_or_create(order=Order.get_order(orderid))
        if imageUrl:
            scan.scanImageRaw = Photo.objects.get(title=imageUrl).file
        scan.scanImageUrl = settings.BASE_URL + imageUrl
        scan.save()  
        data = {'success': True, 'message': 'scan has uploaded successfully'}

    return JsonResponse(data)              