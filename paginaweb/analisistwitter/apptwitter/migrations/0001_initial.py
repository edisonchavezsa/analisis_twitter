# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-12 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweetsanalizado',
            fields=[
                ('id_analisis', models.AutoField(primary_key=True, serialize=False)),
                ('fechaingreso', models.TimeField(blank=True, null=True)),
                ('archvio', models.CharField(blank=True, max_length=200, null=True)),
                ('analizado', models.NullBooleanField()),
            ],
            options={
                'db_table': 'tweetsanalizado',
                'managed': False,
            },
        ),
    ]