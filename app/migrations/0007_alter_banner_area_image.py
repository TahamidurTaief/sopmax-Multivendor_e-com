# Generated by Django 5.0.6 on 2024-05-16 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_banner_area_alter_slider_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner_area',
            name='image',
            field=models.ImageField(upload_to='banner_images'),
        ),
    ]
