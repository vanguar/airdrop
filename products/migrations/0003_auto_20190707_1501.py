# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-07-07 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190707_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='additional_ICO',
            new_name='additional_ico',
        ),
    ]
