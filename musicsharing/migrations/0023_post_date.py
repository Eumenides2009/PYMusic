# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-16 21:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('musicsharing', '0022_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 16, 21, 13, 23, 513812, tzinfo=utc)),
            preserve_default=False,
        ),
    ]