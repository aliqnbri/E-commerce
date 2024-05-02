# Generated by Django 5.0.2 on 2024-04-11 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='product.review'),
        ),
    ]
