# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-24 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0011_auto_20170823_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='artteilnahme',
            name='g_hat_teilgenommen',
            field=models.CharField(default='', max_length=100),
        ),
    ]
