# Generated by Django 2.2.4 on 2019-08-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0015_auto_20190805_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='eta',
            field=models.CharField(blank=True, default=0, max_length=3, null=True),
        ),
    ]