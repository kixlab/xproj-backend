# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_year_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='year_of_birth',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
