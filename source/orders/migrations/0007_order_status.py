# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-24 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20161223_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Criado'), ('completed', 'Finalizado')], default='created', max_length=20),
        ),
    ]
