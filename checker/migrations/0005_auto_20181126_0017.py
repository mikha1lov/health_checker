# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 00:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0004_auto_20181125_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='last_check_time',
            new_name='last_check',
        ),
    ]