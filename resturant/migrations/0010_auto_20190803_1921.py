# Generated by Django 2.2.4 on 2019-08-03 19:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0009_auto_20190803_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='costList',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=[], size=None),
        ),
    ]