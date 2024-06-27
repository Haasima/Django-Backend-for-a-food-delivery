# Generated by Django 4.2.7 on 2024-06-26 05:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0003_remove_useraddress_user_useraddress_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
    ]