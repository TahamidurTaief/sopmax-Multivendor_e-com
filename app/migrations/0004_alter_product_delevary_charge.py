# Generated by Django 5.0.6 on 2024-06-02 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_discount_product_delevary_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='delevary_charge',
            field=models.IntegerField(blank=True, default=150, null=True),
        ),
    ]
