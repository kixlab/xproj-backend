# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-16 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0009_auto_20190316_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newtaggedeffect',
            name='content_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='effect_newtaggedeffects', to='effect.Effect'),
        ),
    ]
