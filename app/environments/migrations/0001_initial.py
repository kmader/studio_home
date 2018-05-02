# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-05-02 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='0', max_length=200)),
                ('name', models.CharField(default='', max_length=200)),
                ('file_name', models.CharField(default='', max_length=200)),
                ('compute_server', models.CharField(max_length=200)),
                ('session_id', models.CharField(max_length=32)),
                ('compute_session', models.CharField(default='NOTSET', max_length=32)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
    ]