"""EpicEvent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app import views

router = routers.SimpleRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('client/', views.ClientList.as_view(), name='client'),
    path('client/<int:pk>/', views.ClientDetail.as_view(), name='client'),
    path('contract/', views.ContractList.as_view(), name='contract'),
    path('contract/<int:pk>/', views.ContractDetail.as_view(), name='contract'),
    path('event/', views.EventList.as_view(), name='event'),
    path('event/<int:pk>/', views.EventDetail.as_view(), name='event'),
]
