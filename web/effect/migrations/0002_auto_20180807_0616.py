# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-07 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='effect',
            old_name='likes',
            new_name='empathy',
        ),
        migrations.AddField(
            model_name='effect',
            name='novelty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='effect',
            name='source',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
    ]