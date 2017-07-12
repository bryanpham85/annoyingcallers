# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 10:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registered_device',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='registered_device',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]