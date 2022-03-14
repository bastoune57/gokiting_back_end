# Generated by Django 4.0.2 on 2022-03-03 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0006_alter_category_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date')),
                ('stop_date', models.DateTimeField(blank=True, verbose_name='start date')),
                ('city', models.CharField(max_length=150, verbose_name='first name')),
                ('country', models.CharField(max_length=150, verbose_name='first name')),
                ('ZIP', models.CharField(blank=True, default=0, max_length=10, verbose_name='first name')),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, default=0.0, max_digits=6, verbose_name='longitude')),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, default=0.0, max_digits=6, verbose_name='longitude')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]