# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-30 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0014_auto_20170827_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='veranstaltung',
            name='datum_anfang',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='veranstaltung',
            name='datum_ende',
            field=models.DateField(blank=True, null=True),
        ),
    ]
