# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions

from checker.models import Url
from checker.serializers import UrlSerializer


class UrlViewSet(viewsets.ModelViewSet):
    """
    list:
    Get url with updated status
    """

    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'patch', 'head']

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == 'list':
            return queryset.update_status()
        return queryset
