# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 09:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caller',
            fields=[
                ('callerId', models.AutoField(primary_key=True, serialize=False)),
                ('country_code', models.CharField(choices=[('VN', 'VN(+84)'), ('US', 'US(+1)')], max_length=5)),
                ('caller_number', models.CharField(max_length=11)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ac_caller',
                'ordering': ('registered_date',),
            },
        ),
        migrations.CreateModel(
            name='Caller_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_type', models.IntegerField(choices=[(1, 'Private'), (2, 'Global')])),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('caller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Caller')),
            ],
            options={
                'db_table': 'ac_caller_category',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ac_category',
                'ordering': ('created_date',),
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('deviceId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('devicePlatform', models.CharField(choices=[('Android', 'Android'), ('iOS', 'iOS'), ('Blackberry', 'Blackberry')], max_length=20)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1)),
                ('installed_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ac_device',
                'ordering': ('installed_date',),
            },
        ),
        migrations.AddField(
            model_name='caller_category',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Category'),
        ),
        migrations.AddField(
            model_name='caller',
            name='category',
            field=models.ManyToManyField(through='api.Caller_Category', to='api.Category'),
        ),
        migrations.AddField(
            model_name='caller',
            name='registered_by_device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Device'),
        ),
        migrations.AddIndex(
            model_name='caller_category',
            index=models.Index(fields=['caller_id', 'category_id'], name='caller_category_index'),
        ),
        migrations.AddIndex(
            model_name='caller',
            index=models.Index(fields=['country_code', 'caller_number'], name='caller_index'),
        ),
    ]
