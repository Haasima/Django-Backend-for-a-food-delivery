# Generated by Django 4.2.7 on 2024-06-24 07:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0002_alter_city_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='user',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
    ]
