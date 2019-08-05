# Generated by Django 2.2.4 on 2019-08-05 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0013_auto_20190804_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('service_tax', models.DecimalField(decimal_places=10, default=0, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
