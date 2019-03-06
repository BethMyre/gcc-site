# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-24 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
        ('contest', '0007_add_home_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='school',
            field=models.ForeignKey(default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='contestants', to='schools.School'),
        ),
    ]
