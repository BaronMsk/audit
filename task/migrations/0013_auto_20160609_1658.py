# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_hostdetails_detail_host_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_data_create',
            field=models.DateField(auto_now=True),
        ),
    ]