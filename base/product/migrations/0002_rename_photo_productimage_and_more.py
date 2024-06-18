# Generated by Django 4.2.7 on 2024-06-08 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_initial_categories(apps, shem_editor):
    Category = apps.get_model('product', 'Category')
    
    # создание основных категорий
    male = Category.objects.create(name='Male')
    female = Category.objects.create(name='Female')
    kids = Category.objects.create(name='Kids')
    other = Category.objects.create(name='Other')
    
    # создание подкатегорий для Kids
    boys = Category.objects.create(name='Boys', parent=kids)
    girls = Category.objects.create(name='Girls', parent=kids)
    
    subcategories = ['Accessories', 'Clothing', 'Backpacks']
    categories = [male, female, boys, girls]
    
    for subcategory in subcategories:
        for category in categories:
            Category.objects.create(name=subcategory, parent=category)
            
    # дополнительные категории для Male и Female
    Category.objects.create(name='Jewelry', parent=male)
    Category.objects.create(name='Jewelry', parent=female)
    
    # дополнительные категории для boys и girls
    Category.objects.create(name='Toys', parent=boys)
    Category.objects.create(name='Toys', parent=girls)
    
    # создание подкатегорий для other
    electronics = Category.objects.create(name='Electronics', parent=other)
    
    electronic_categories = ['smartphones', 'laptops', 'televisions', 'tablets']
    
    for el_cat in electronic_categories:
        Category.objects.create(name=el_cat.capitalize(), parent=electronics)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Photo',
            new_name='ProductImage',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='photo',
            new_name='image',
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('status', models.CharField(choices=[('ORDER ON THE WAY', 'Order on the way'), ('DELIVERED', 'Delivered')], default='ORDER ON THE WAY', max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(null=True)),
                ('courier', models.ForeignKey(limit_choices_to={'role': 'COURIER'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='couriers', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='product.category')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category'),
        ),
        migrations.RunPython(create_initial_categories),
    ]