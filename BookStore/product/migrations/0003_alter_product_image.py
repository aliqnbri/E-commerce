# Generated by Django 5.0.2 on 2024-03-01 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_author_is_deleted_alter_category_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/products/'),
        ),
    ]
