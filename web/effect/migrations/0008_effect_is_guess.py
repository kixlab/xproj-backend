# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-02 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0007_effect_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='effect',
            name='is_guess',
            field=models.BooleanField(default=False),
        ),
    ]