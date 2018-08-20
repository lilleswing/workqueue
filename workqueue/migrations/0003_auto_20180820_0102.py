# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-20 01:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workqueue', '0002_workunit_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='workunit',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 20, 1, 2, 34, 26080), verbose_name='end_time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workunit',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 20, 1, 2, 42, 841014), verbose_name='start_time'),
            preserve_default=False,
        ),
    ]
