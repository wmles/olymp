# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-17 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0004_auto_20170605_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='teilnahme',
            name='nur_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]