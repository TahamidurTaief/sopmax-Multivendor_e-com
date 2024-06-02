# Generated by Django 5.0.6 on 2024-06-02 12:13

import ckeditor.fields
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner_Area',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='banner_images')),
                ('discount_deal', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('quote', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('discount', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
                ('image', models.ImageField(upload_to='brand_images')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
                ('code', models.CharField(blank='', default='', max_length=10, null='')),
            ],
        ),
        migrations.CreateModel(
            name='CuponCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Main_Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Size',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='media/slider_images')),
                ('link', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
                ('main_Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.main_category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
                ('model_name', models.CharField(blank='', default='', max_length=100, null='')),
                ('Product_information', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('availability', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('discount_price', models.IntegerField(blank=True, default=0, null=True)),
                ('discount', models.IntegerField(blank=True, default=0, null=True)),
                ('tags', models.CharField(blank='', default='', max_length=100, null='')),
                ('featured_image', models.CharField(blank='', default='', max_length=200, null='')),
                ('slug', models.SlugField(blank=True, default='', max_length=500, null=True)),
                ('brand', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
                ('color', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.color')),
                ('size', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product_size')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.section')),
            ],
            options={
                'db_table': 'app_Product',
            },
        ),
        migrations.CreateModel(
            name='Additional_Information',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(blank='', default='', max_length=100, null='')),
                ('value', models.CharField(blank='', default='', max_length=100, null='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.CharField(blank='', default='', max_length=200, null='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank='', default='', max_length=100, null='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
    ]
