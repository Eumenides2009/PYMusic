# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-07 03:22
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musicsharing', '0013_auto_20160407_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
