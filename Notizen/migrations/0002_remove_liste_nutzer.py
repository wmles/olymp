# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-29 15:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notizen', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liste',
            name='nutzer',
        ),
    ]