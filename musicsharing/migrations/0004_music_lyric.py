# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-27 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicsharing', '0003_auto_20160324_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='lyric',
            field=models.FileField(null=True, upload_to='music_lyric'),
        ),
    ]
