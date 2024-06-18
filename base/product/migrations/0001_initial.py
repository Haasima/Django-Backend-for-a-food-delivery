# Generated by Django 4.2.7 on 2024-06-07 00:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('rate', models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='address.shopaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('rate', models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('status', models.CharField(choices=[('OUT OF STOCK', 'Out of stock'), ('IN STOCK', 'In stock')], default='OUT OF STOCK', max_length=50)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ManyToManyField(related_name='products', to='product.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=product.models.product_upload_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='product.product')),
            ],
        ),
    ]