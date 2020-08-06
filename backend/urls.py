"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from users import views
from order import views as order_views
from backend import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin part
    path('admin/', admin.site.urls),
    
    # api part
    path('api/auth/', include('users.urls')),
    path('api/order/', include('order.urls')),
    path('api/scan/', include('scan.urls')),

    # web part
    path(r'ajax_login/', views.ajax_login, name = "ajax_login"),
    path(r'ajax_register/', views.ajax_register, name = "ajax_register"),
    path(r'ajax_logout/', views.ajax_logout, name="ajax_logout"),
    path(r'ajax_order/', order_views.ajax_order, name="ajax_order"),
    path(r'', views.home, name = "home"),
    path(r'planprices/', views.planprices, name = "planprices"),
    path(r'ownguestmapp/', views.ownguestmapp, name="ownguestmapp"),
    path(r'guestmapp/', views.guestmapp, name = "guestmapp"),
    path(r'newpassword/', views.newpassword),

    # media part
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
