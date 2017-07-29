# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-27 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wettbewerbe', '0007_auto_20170727_0739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artkategorie',
            options={'verbose_name': 'Art von Wettbewerbskategorien', 'verbose_name_plural': 'Arten der Wettbewerbskategorien'},
        ),
        migrations.AlterField(
            model_name='artkategorie',
            name='plural',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]