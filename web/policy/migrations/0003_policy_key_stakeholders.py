# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-15 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0002_auto_20180815_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='key_stakeholders',
            field=models.TextField(default=''),
        ),
    ]
