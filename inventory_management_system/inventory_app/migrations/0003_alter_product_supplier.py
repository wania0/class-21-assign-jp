# Generated by Django 5.1.1 on 2024-10-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0002_rename_cat_id_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ManyToManyField(related_name='products', to='inventory_app.supplier'),
        ),
    ]
