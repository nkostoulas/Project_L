# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20170113_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='locale',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
