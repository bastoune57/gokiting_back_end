# Generated by Django 4.0.2 on 2022-04-02 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_alter_location_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=6, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90)], verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(decimal_places=4, max_digits=7, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180)], verbose_name='longitude'),
        ),
    ]
