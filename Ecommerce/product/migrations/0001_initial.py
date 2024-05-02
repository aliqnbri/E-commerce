# Generated by Django 5.0.2 on 2024-04-11 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('on', 'Active'), ('off', 'Deactive')], default='on', max_length=8)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('on', 'Active'), ('off', 'Deactive')], default='on', max_length=8)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/category/')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('on', 'Active'), ('off', 'Deactive')], default='on', max_length=8)),
                ('is_deleted', models.BooleanField(default=False)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comment', models.TextField(blank=True, max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customerprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('on', 'Active'), ('off', 'Deactive')], default='on', max_length=8)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/products/')),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='product.review')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='product.product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.customerprofile')),
            ],
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='product_cat_name_4f76a1_idx'),
        ),
    ]
