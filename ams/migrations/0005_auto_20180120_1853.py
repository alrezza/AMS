# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-20 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0004_auto_20180120_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownership',
            name='status',
            field=models.CharField(choices=[('Booked asset', 'Booked asset'), ('Approved', 'Approved')], max_length=20),
        ),
    ]