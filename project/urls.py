"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from auth.views import AuthTokenViewSet
from checker.views import UrlViewSet

schema_view = get_swagger_view(title='Health checker API')

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'auth', AuthTokenViewSet, base_name='auth')
router.register(r'url', UrlViewSet)

urlpatterns = [
    url(r'^$', schema_view),
    url(r'^v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
