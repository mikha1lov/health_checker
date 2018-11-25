# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from checker.models import Url


class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'status', 'is_paused')


admin.site.register(Url, UrlAdmin)
