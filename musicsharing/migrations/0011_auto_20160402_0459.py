# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-02 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicsharing', '0010_auto_20160402_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='picture',
            field=models.ImageField(default='list_image/default.jpg', upload_to='list_image'),
        ),
    ]
