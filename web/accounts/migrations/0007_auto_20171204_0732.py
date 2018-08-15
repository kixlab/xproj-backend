# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20171204_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other'), ('', 'Rather not say')], default='', max_length=10, verbose_name='Gender (성별)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(choices=[('employed', 'Employed'), ('self-employed', 'Self-employed'), ('unemployed', 'Unemployed'), ('homemaker', 'Homemaker'), ('student', 'Student'), ('retired', 'Retired'), ('other', 'Other')], default='', max_length=20, verbose_name='Occupation (직업)'),
        ),
    ]