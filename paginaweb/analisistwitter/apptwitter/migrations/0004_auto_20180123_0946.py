# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-23 14:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptwitter', '0003_auto_20180123_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentosexcel',
            name='fechaingreso',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 23, 9, 46, 25, 759463)),
        ),
        migrations.AlterField(
            model_name='documentosgoogle',
            name='fechaingreso',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 23, 9, 46, 25, 758446)),
        ),
    ]