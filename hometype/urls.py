from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'list', views.HomeTypeViewSet.as_view({'get': 'list'})),
]
