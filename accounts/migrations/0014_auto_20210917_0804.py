# Generated by Django 3.2.6 on 2021-09-17 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_workdetails_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='rating_count',
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]