# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-04 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0008_auto_20170727_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nutzer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Grundgeruest.Nutzerprofil'),
        ),
    ]
