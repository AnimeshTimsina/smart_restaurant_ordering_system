# Generated by Django 2.2.4 on 2019-08-03 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0002_auto_20190803_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='dateOfCreation',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
