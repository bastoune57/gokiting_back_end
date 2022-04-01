# Generated by Django 4.0.2 on 2022-04-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_alter_location_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=6, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(decimal_places=4, max_digits=6, verbose_name='longitude'),
        ),
    ]
