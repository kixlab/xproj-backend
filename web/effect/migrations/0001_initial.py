# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-25 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stakeholdergroup', '0001_initial'),
        ('policy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isBenefit', models.IntegerField(default=0)),
                ('stakeholder_detail', models.TextField()),
                ('description', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='effects', to='policy.Policy')),
                ('stakeholder_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='effects', to='stakeholdergroup.StakeholderGroup')),
            ],
        ),
    ]