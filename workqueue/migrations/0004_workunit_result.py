# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-20 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workqueue', '0003_auto_20180820_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='workunit',
            name='result',
            field=models.TextField(null=True),
        ),
    ]
