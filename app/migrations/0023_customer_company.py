# Generated by Django 4.1.6 on 2023-05-04 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_customer_mail_customer_mail_list_bcc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
