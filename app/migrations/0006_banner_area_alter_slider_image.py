# Generated by Django 5.0.6 on 2024-05-16 02:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_slider_brand_name_remove_slider_discount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='banner_area',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='media/banner_images')),
                ('discount_deal', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('quote', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('discount', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=models.ImageField(upload_to='media/slider_images'),
        ),
    ]