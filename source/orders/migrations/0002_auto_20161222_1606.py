# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-22 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercheckout',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
