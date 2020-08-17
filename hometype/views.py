from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from decouple import config
from hometype.models import HomeType

class HomeTypeViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = (permissions.IsAuthenticated,)
    
    def list(self, request, *args, **kwargs):
        hometypes = HomeType.objects.all()    
        return JsonResponse({
            "success": True,
            "message": "success to get home type list",
            "errCode": -1,
            "data": [ hometype.to_dict() for hometype in hometypes]
        }, status=status.HTTP_200_OK)