# Generated by Django 4.2.7 on 2024-06-04 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('token_auth', '0002_city_country_customuser_role_useraddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='apartment_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='country', chained_model_field='country', on_delete=django.db.models.deletion.CASCADE, related_name='city', to='token_auth.city'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='code_number',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country', to='token_auth.country'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='entrance_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
    ]
