# Generated by Django 5.1.4 on 2025-01-24 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_name', models.CharField(max_length=255, null=True)),
                ('Description', models.CharField(max_length=255, null=True)),
                ('Price', models.CharField(max_length=255, null=True)),
                ('Product_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('Category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecommerce_App.categories')),
            ],
        ),
    ]
