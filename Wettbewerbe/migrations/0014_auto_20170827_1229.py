# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-27 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0013_auto_20170827_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teilnahme',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Wettbewerbe.Person'),
        ),
        migrations.AlterField(
            model_name='teilnahme',
            name='veranstaltung',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Wettbewerbe.Veranstaltung'),
        ),
    ]
