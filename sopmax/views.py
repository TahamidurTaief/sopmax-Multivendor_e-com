from django.shortcuts import redirect, render
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
def base(request):
    return render(request, 'base.html')

def error404(request):
    return render(request, 'error/404.html')


def Account(request):
    return render(request, 'account/my-account.html')


def Home(request):
    sliders = Slider.objects.all().order_by('-id')[0:5]
    banner_areas = banner_area.objects.all().order_by('-id')[0:3]


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
        'top_deals_product': top_deals_product
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