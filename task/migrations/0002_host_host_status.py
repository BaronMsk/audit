# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-08 13:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='host_status',
            field=models.BooleanField(default=datetime.datetime(2016, 6, 8, 13, 40, 20, 338103, tzinfo=utc)),
            preserve_default=False,
        ),
    ]