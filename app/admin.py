from django.contrib import admin
from .models import *



class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class ProductAdmin(admin.ModelAdmin):
    inlines = [Product_Images, Additional_Informations]
    list_display = ['name', 'price', 'quantity', 'category', 'section']
    list_editable = ['price', 'quantity', 'category', 'section']



admin.site.register(Slider)
admin.site.register(banner_area)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Section)
admin.site.register(Product,ProductAdmin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)