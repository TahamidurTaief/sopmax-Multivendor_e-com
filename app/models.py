from django.db import models
import uuid 
from ckeditor.fields import RichTextField # type: ignore
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User




class Slider(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='media/slider_images')
    link = models.CharField(max_length=300, null=True, blank=True)

    # def __str__(self):
    #     return self.link


class Banner_Area(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='banner_images')
    discount_deal = models.CharField(max_length=100, default="", null=True, blank=True)
    quote = models.CharField(max_length=100, default="", null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.quote
    


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="", null="", blank="") 
    image = models.ImageField(upload_to='brand_images')

    def __str__(self):
        return self.name
    



class Main_Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="", null="", blank="") 

    def __str__(self):
        return self.name




class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    main_Category= models.ForeignKey(Main_Category,related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="", null="", blank="") 
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

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
    model_name = models.CharField(max_length=100, default="", null="", blank="")
    Product_information = RichTextField(null=True, blank=True)
    Description = RichTextField(null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    availability = models.IntegerField(default=0, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    # delevary_charge = models.IntegerField(default=150, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, default="")
    tags = models.CharField(max_length=100, default="", null="", blank="")
    featured_image =models.ImageField(upload_to='product_images', null=True, blank=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def discounted_price(self):
        try:
            price = int(self.price)
            discount = int(self.discount)
        except (TypeError, ValueError):
            return None
        
        if price is None:
            return None
        if discount is None or discount == 0:
            return price
        return max(price - (price * discount / 100), 0)


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




class CuponCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    

class Product_Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return self.product.name 
    

class Additional_Information(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, default="", null="", blank="")
    value = models.CharField(max_length=100, default="", null="", blank="")

    def __str__(self):
        return self.product.name 
    




class Color(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="", null="", blank="") 
    code = models.CharField(max_length=10, default="", null="", blank="") 

    def __str__(self):
        return self.name




class Product_Size(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  null=True, blank=True)
    name = models.CharField(max_length=100, default="", null="", blank="") 

    def __str__(self):
        return self.name






from django.contrib.auth.models import User

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.TextField(default='', null=True, blank=True)
    first_name = models.CharField(max_length=100, default='', null=True, blank=True)
    last_name = models.CharField(max_length=100, default='', null=True, blank=True)
    company_name = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, default='', null=True, blank=True)
    address = models.CharField(max_length=255, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=255, blank=True, default='')
    town_city = models.CharField(max_length=100, default='', null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, default='')
    postcode = models.CharField(max_length=20, default='', null=True, blank=True)
    phone = models.CharField(max_length=20, default='', null=True, blank=True)
    email = models.CharField(max_length=100, default='', null=True, blank=True)
    tranjection_number = models.CharField(max_length=100, default='', null=True, blank=True)
    tranjection_id = models.CharField(max_length=100, default='', null=True, blank=True)
    note = models.TextField(blank=True, default='', null=True)
    cart_total_amount = models.CharField(max_length=100, default="", null=True, blank=True)
    coupon_discount_price = models.CharField(max_length=100, default=0, null=True, blank=True)
    shipping_cost = models.CharField(max_length=10, default="", null=True, blank=True)
    order_total = models.CharField(max_length=10, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for {self.first_name} {self.last_name}"


class PreOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.TextField(default='', null=True, blank=True)
    first_name = models.CharField(max_length=100, default='', null=True, blank=True)
    last_name = models.CharField(max_length=100, default='', null=True, blank=True)
    company_name = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, default='', null=True, blank=True)
    address = models.CharField(max_length=255, default='', null=True, blank=True)
    address_2 = models.CharField(max_length=255, blank=True, default='')
    town_city = models.CharField(max_length=100, default='', null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, default='')
    postcode = models.CharField(max_length=20, default='', null=True, blank=True)
    phone = models.CharField(max_length=20, default='', null=True, blank=True)
    email = models.CharField(max_length=100, default='', null=True, blank=True)
    tranjection_number = models.CharField(max_length=100, default='', null=True, blank=True)
    tranjection_id = models.CharField(max_length=100, default='', null=True, blank=True)
    note = models.TextField(blank=True, default='', null=True)
    cart_total_amount = models.CharField(max_length=100, default="", null=True, blank=True)
    coupon_discount_price = models.CharField(max_length=100, default=0, null=True, blank=True)
    shipping_cost = models.CharField(max_length=10, default="", null=True, blank=True)
    order_total = models.CharField(max_length=10, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for {self.tranjection_id}"
    


class OrderTracking(models.Model):
    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE, related_name='tracking')
    order_received = models.DateField()
    order_processed = models.DateField()
    manufacturing_in_progress = models.DateField()
    order_dispatched = models.DateField()
    order_delivered = models.DateField()

    def __str__(self):
        return f"Tracking for {self.checkout.product_name}"