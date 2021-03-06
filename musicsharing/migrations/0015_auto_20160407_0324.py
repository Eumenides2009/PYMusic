# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-07 03:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicsharing', '0014_auto_20160407_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('G', 'Gay'), ('L', 'Lesbian'), ('B', 'Bisexual'), ('T', 'Transgender'), ('D', 'undefined :)')], default='D', max_length=10),
        ),
    ]
