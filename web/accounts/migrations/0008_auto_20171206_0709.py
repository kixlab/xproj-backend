# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20171204_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'female'), ('male', 'male'), ('other', 'other'), ('', 'rather not say')], default='', max_length=10, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spatial.Area', verbose_name='area of residence'),
        ),
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(choices=[('employed', 'employed'), ('self-employed', 'self-employed'), ('unemployed', 'unemployed'), ('homemaker', 'homemaker'), ('student', 'student'), ('retired', 'retired'), ('other', 'other')], default='', max_length=20, verbose_name='occupation'),
        ),
        migrations.AlterField(
            model_name='user',
            name='year_of_birth',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='year of birth'),
        ),
    ]