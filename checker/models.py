# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from threading import Thread
from Queue import Queue

from django.conf import settings
from django.db import models
from requests.exceptions import ConnectionError, ReadTimeout


class UrlQuerySet(models.QuerySet):
    def update_status(self):

        def _async_check():
            while True:
                obj = q.get()
                obj.update_status()
                q.task_done()

        urls = self.filter(is_paused=False)
        concurrent = urls.count()
        q = Queue(concurrent * 2)
        for i in range(concurrent):
            t = Thread(target=_async_check)
            t.daemon = True
            t.start()

        for url in self.all():
            q.put(url)
        q.join()

        return urls


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
    last_check_time = models.DateTimeField(null=True, blank=True)
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
        self.save()
        return self.status
