# Generated by Django 4.2.7 on 2024-06-26 00:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_orderproduct_order_quantity_alter_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]