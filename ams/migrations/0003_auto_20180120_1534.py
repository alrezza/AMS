# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-20 08:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0002_auto_20180120_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Booked', 'booked asset'), ('Approved', 'approved asset')], max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='asset',
            name='status',
        ),
        migrations.AddField(
            model_name='ownership',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ams.Asset'),
        ),
        migrations.AddField(
            model_name='ownership',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ams.Employee'),
        ),
    ]
