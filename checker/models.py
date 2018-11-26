# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

import requests
import gevent

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from requests.exceptions import ConnectionError, ReadTimeout


class UrlQuerySet(models.QuerySet):
    def update_status(self):
        threshold = timezone.now() - timedelta(
            seconds=settings.MINIMAL_CHECK_INTERVAL
        )

        urls = self.filter(is_paused=False).filter(Q(last_check__lt=threshold) | Q(last_check__isnull=True))
        if urls:
            jobs = [gevent.spawn(url.update_status) for url in urls]
            gevent.joinall(jobs, timeout=2)

        return self


class Url(models.Model):
    OK = 'ok'
    ERROR = 'error'

    STATUSES = (
        (OK, 'OK'),
        (ERROR, 'Error'),
    )

    STATUS_CODES_MAP = {
        200: OK
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='urls')
    url = models.URLField()
    status = models.CharField(choices=STATUSES, max_length=100, null=True, blank=True)
    last_check = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)

    objects = models.Manager.from_queryset(UrlQuerySet)()

    def get_url_status_code(self):
        response = requests.head(self.url, timeout=settings.CHECKER_REQUEST_TIMEOUT)
        return response.status_code

    def update_status(self):
        status_code = None
        try:
            status_code = self.get_url_status_code()
        except (ConnectionError, ReadTimeout):
            pass
        self.status = self.STATUS_CODES_MAP.get(status_code, self.ERROR)
        self.last_check = timezone.now()
        self.save()
        return self.status
