# Generated by Django 4.0.2 on 2022-03-03 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0008_remove_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='ZIP',
            field=models.CharField(blank=True, default=0, max_length=10, verbose_name='ZIP'),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(max_length=150, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(max_length=150, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=5, default=0.0, max_digits=6, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='stop_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='stop date'),
        ),
    ]