# Generated by Django 4.0.2 on 2022-03-03 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0012_remove_timeperiod_stop_date_timeperiod_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baselocations', to='instructors.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baselocations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'location')},
            },
        ),
    ]
