# Generated by Django 4.1.6 on 2023-03-17 04:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_myfile_day_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_price',
            name='date',
            field=models.DateField(db_index=True, default=datetime.date.today),
        ),
    ]
