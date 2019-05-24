# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-15 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpolicy', '0007_auto_20180903_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpolicy',
            name='final_opinion',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='userpolicy',
            name='final_stance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userpolicy',
            name='initial_opinion',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='userpolicy',
            name='initial_stance',
            field=models.IntegerField(default=0),
        ),
    ]
