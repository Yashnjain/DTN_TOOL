# Generated by Django 4.1.6 on 2023-06-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_customer_customer_code_terminal_location_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cust_price',
            name='sap',
            field=models.BooleanField(default=False),
        ),
    ]
