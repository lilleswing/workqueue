# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-20 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workqueue', '0005_workunit_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workunit',
            name='end_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='end_time'),
        ),
        migrations.AlterField(
            model_name='workunit',
            name='key',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='workunit',
            name='start_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='start_time'),
        ),
    ]