from django.db import models
import uuid 
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save





class Slider(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='media/slider_images')
    link = models.CharField(max_length=300, null=True, blank=True)

    # def __str__(self):
    #     return self.link


class banner_area(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='banner_images')
    discount_deal = models.CharField(max_length=100, default="", null=True, blank=True)
    quote = models.CharField(max_length=100, default="", null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.quote




class Main_Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="", null="", blank="") 

    def __str__(self):
        return self.name




class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    main_Category= models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="", null="", blank="") 

    def __str__(self):
        return self.name + "-- " + self.main_Category.name
    


class Sub_Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="", null="", blank="") 

    def __str__(self):
        return self.name+ "-- " + self.category.name
    


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="", null="", blank="") 

    def __str__(self):
        return self.name
    

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="", null="", blank="")
    price = models.IntegerField(default=0, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    Product_information = RichTextField(null=True, blank=True)
    Description = RichTextField(null=True, blank=True)
    model_name = models.CharField(max_length=100, default="", null="", blank="")
    availability = models.IntegerField(default=0, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, default="", null="", blank="")
    featured_image = models.CharField(max_length=200, default="", null="", blank="")
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)


    def __str__(self): 
        return self.name + "-- " + self.category.name
    

    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"



def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)

    

class Product_Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=200, default="", null="", blank="")

    def __str__(self):
        return self.product.name 
    

class Additional_Information(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, default="", null="", blank="")
    value = models.CharField(max_length=100, default="", null="", blank="")

    def __str__(self):
        return self.product.name 