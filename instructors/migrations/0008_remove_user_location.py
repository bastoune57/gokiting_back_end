# Generated by Django 4.0.2 on 2022-03-03 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0007_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
    ]
