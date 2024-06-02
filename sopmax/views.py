from django.http import JsonResponse
from django.shortcuts import redirect, render
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum
from django.contrib.auth.decorators import login_required
from cart.cart import Cart #type: ignore

# Create your views here.
def base(request):
    return render(request, 'base.html')

def error404(request):
    return render(request, 'error/404.html')


def Account(request):
    return render(request, 'account/my-account.html')


def Home(request):
    sliders = Slider.objects.all().order_by('-id')[0:5]
    banner_areas = Banner_Area.objects.all().order_by('-id')[0:3]


    main_cat = Main_Category.objects.all()
    sub_cat = Sub_Category.objects.all()
    cat = Category.objects.all()
    top_deals_product = Product.objects.filter(section__name='Top Deals Of The Day')


    

    context = {
        'sliders': sliders,
        'banner_areas' : banner_areas,
        'main_cat': main_cat,
        'sub_cat': sub_cat,
        'cat': cat,
        'top_deals_product': top_deals_product,
    }
    
    return render(request, 'main/home.html', context)



def ProductDetail(request, slug):
    product = Product.objects.filter(slug=slug)

    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')
    

    context = {
        'product': product
    }


    return render(request, "product/product_details.html", context)



def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exists')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exists')
            return redirect('login')

        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_superuser = False
        user.save()
        print('User created')

        return redirect('login')
    


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('logusername')
        password = request.POST.get('logpassword')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    # return render(request, 'account/my-account.html')


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')  # Replace 'home' with your desired redirect URL




def About(request):
    return render(request, 'main/about.html')

def Contact(request):
    return render(request, 'main/contact.html')


def Products(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    sizes = Product_Size.objects.all()
    brand = Brand.objects.all()


   # FILTER WITH CATEGORY
    CategoryID = request.GET.get('categoryID')
    ColorID = request.GET.get('colorID')
    FilterPrice = request.GET.get('FilterPrice')
    size_filters = request.GET.getlist('size')
    brandID = request.GET.get('brandID')
    
    


    # FILTER WITH PRICE RANGE
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    
    elif CategoryID:
        product = Product.objects.filter(category__id=CategoryID)
    
    elif ColorID:
        product = Product.objects.filter(color__id=ColorID)
    
    elif size_filters:
        size_ids = [int(size) for size in size_filters]
        product = Product.objects.filter(size__id__in=size_ids)
    
    elif brandID:
        product = Product.objects.filter(brand__id=brandID)
    
    else:
        product = Product.objects.all()

    
 

    context = {
        'category': category,
        'product': product,
        'color': color,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,
        'sizes': sizes,
        'brand': brand,
    }

    return render(request, 'product/product.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()


    t = render_to_string('ajax/product.html', {'product': allProducts})
    print(t)

    return JsonResponse({'data': t})





@login_required(login_url="/acounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/acounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/acounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/acounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/acounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/acounts/login")
def cart_detail(request):
    # cart = request.session.get('cart')
    # product = Product.objects.all()

    # context = {
    #     'product': product,
    # }

    return render(request, 'cart/cart.html')