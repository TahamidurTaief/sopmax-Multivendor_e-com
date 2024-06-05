from django.contrib import admin
from .models import *


class ProductImagesInline(admin.TabularInline):
    model = Product_Image

class AdditionalInformationsInline(admin.TabularInline):
    model = Additional_Information

class ProductColorInline(admin.TabularInline):
    model = Color

class ProductSizeInline(admin.TabularInline):
    model = Product_Size

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline, AdditionalInformationsInline, ProductColorInline, ProductSizeInline]
    list_display = ['name', 'price', 'quantity', 'category', 'section']
    list_editable = ['price', 'quantity', 'category', 'section']



admin.site.register(Slider)
admin.site.register(Banner_Area)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Section)
admin.site.register(Product,ProductAdmin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(Color)
admin.site.register(Product_Size)
admin.site.register(Brand)
admin.site.register(Checkout)
admin.site.register(PreOrder)


@admin.register(CuponCode)
class CuponCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount','active')
    list_filter = ('active', 'discount')
    search_fields = ('code',)