# Create your views here.
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from scan.models import ScanTable, ScanDetailsTable
from scan.serializers import ScanTableSerializer, ScanDetailsTableSerializer


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
