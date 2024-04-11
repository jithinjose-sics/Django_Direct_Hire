# Generated by Django 3.2.6 on 2024-04-08 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_customer_adharno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='adharno',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator('^\\d{12}$', message='Aadhar number must be a 12-digit number')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='adharno',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator('^\\d{12}$', message='Aadhar number must be a 12-digit number')]),
        ),
    ]
