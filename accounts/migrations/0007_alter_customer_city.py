# Generated by Django 3.2.6 on 2021-08-28 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_employee_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(choices=[('', 'CITY'), ('TVM', 'TVM'), ('CALICUT', 'CALICUT'), ('KOCHIN', 'KOCHIN')], max_length=200, null=True),
        ),
    ]