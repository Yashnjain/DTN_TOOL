# Generated by Django 4.1.6 on 2023-03-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_cust_price_base_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_price',
            name='base_price',
            field=models.FloatField(),
        ),
    ]