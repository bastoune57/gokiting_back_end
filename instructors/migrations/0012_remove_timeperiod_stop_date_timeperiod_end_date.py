# Generated by Django 4.0.2 on 2022-03-03 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0011_alter_timeperiod_start_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeperiod',
            name='stop_date',
        ),
        migrations.AddField(
            model_name='timeperiod',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='end date'),
        ),
    ]