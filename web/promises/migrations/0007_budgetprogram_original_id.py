# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 06:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0006_auto_20171116_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetprogram',
            name='original_id',
            field=models.CharField(default='', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]