# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-13 10:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('effect', '0003_auto_20180813_1006'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Novelty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='novelty', to='effect.Effect')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='novelty', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
