# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-07 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stakeholdergroup', '0001_initial'),
        ('userpolicy', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpolicy',
            old_name='stakeholder',
            new_name='stakeholder_detail',
        ),
        migrations.RemoveField(
            model_name='userpolicy',
            name='is_stakeholder',
        ),
        migrations.RemoveField(
            model_name='userpolicy',
            name='stance',
        ),
        migrations.AddField(
            model_name='userpolicy',
            name='stakeholder_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userpolicy', to='stakeholdergroup.StakeholderGroup'),
        ),
    ]