# Generated by Django 4.1.6 on 2023-06-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_cust_price_sap_customer_sap'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='rack',
            field=models.BooleanField(default=False),
        ),
    ]
