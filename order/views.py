from django.http import JsonResponse
# Create your views here.
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from scan.models import ScanTable
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ['post', 'get']
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        orders = self.get_queryset()
        orderses = []
        for order in orders:
            query = order.to_dict()
            try:
                scans = ScanTable.objects.get(order = order.id)
                query.update({"scan":scans.to_dict()})
            except:
                query.update({"scan":[]})
            orderses.append(query)

        return JsonResponse({
            "success": True,
            "message": "success to get order list",
            "errCode": -1,
            "data": orderses
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)
        return JsonResponse({
            "success": True,
            "message": "success to create new order",
            "errCode": -1,
            "data": order.to_dict()
        }, status=status.HTTP_200_OK)


class OrderCommit(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        order_id = self.request.data['order_id']
        status = self.request.data['status']

        try:
            order = Order.objects.get(id=order_id)
        except:
            return JsonResponse({
                'success': False,
                'message': 'Order is not exist',
                'errCode': -1,
                'data': None
            })

        order.status = status
        order.save()
        return JsonResponse({
            'success': True,
            'message': 'success to update order status',
            'errCode': -1,
            'data': None
        })


def ajax_order(request):
    return JsonResponse({'status':200})