# Generated by Django 5.0.2 on 2024-02-17 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Shop Name')),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=12, verbose_name='Phone Number')),
                ('locations', models.TextField(verbose_name='Locations')),
                ('extra', models.TextField(verbose_name='Extra Info')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='media/logos/')),
            ],
        ),
    ]
