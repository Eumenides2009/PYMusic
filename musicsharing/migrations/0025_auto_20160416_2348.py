# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-16 23:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicsharing', '0024_auto_20160416_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Post',
            new_name='post',
        ),
    ]
