from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

# Create your views here.
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from order.models import Order, Billing
from scan.models import ScanTable
from order.serializers import OrderSerializer
from decouple import config
import stripe

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
                query.update({"scan":{}})
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
        billing = Billing.objects.get(order=order)
        
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer = stripe.Customer.create(
                email = order.user.email,
                description="Customer",
            )
            billing_str = billing.expiry_date
            exp_date = billing_str.split("/")
            if exp_date.__len__() != 2:
                order.delete()
                return JsonResponse({
                'success': False,
                'message': 'Fail to create order',
                'errCode': -1,
                'data': None,
            })
            token = stripe.Token.create(
                card={
                    "number": billing.card_number,
                    "exp_month": exp_date[0],
                    "exp_year": "20" + exp_date[1],
                    "cvc": str(billing.cvv),
                },
            )
            
            # test
            # token = stripe.Token.create(
            #     card={
            #         "number": "4242424242424242",
            #         "exp_month": 8,
            #         "exp_year": 2021,
            #         "cvc": "314",
            #     },
            # )
            stripe.Customer.create_source(
                customer.id,
                source=token,
            )
            stripe.Charge.create(
                customer = customer.id,
                amount = int(order.price),
                currency = 'usd',
                description = 'description'
            )

        except stripe.error.StripeError:
            order.delete()
            return JsonResponse({
                'success': False,
                'message': 'Fail to create order',
                'errCode': -1,
                'data': None,
                
            })
        

        return JsonResponse({
            "success": True,
            "message": "success to create new order",
            "errCode": -1,
            "data": order.to_dict(),
        }, status=status.HTTP_200_OK)


class OrderCommit(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        order_id = self.request.data['order_id']
        status = self.request.data['status']
        order.status = status
        order.save()
        return JsonResponse({
            'success': True,
            'message': 'success to update order status',
            'errCode': -1,
            'data': None
        })

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'BluePrint',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '3000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelledView(TemplateView):
    template_name = 'cancelled.html'