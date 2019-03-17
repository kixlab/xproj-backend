# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-16 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('effect', '0008_effect_is_guess'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewTaggedEffect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='effect.Effect')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='effect_newtaggedeffect_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='effect.NewTag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='effect',
            name='new_tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='effect.NewTaggedEffect', to='effect.NewTag', verbose_name='Tags'),
        ),
    ]