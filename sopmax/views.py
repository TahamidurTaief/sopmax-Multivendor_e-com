from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cart.cart import Cart #type: ignore
from django.contrib.auth.models import AnonymousUser





# Create your views here.
def base(request):
    category = Category.objects.all()

    context = {
        'category': category
    }
    return render(request, 'base.html', context)






def error404(request):
    return render(request, 'error/404.html')

@login_required(login_url="/accounts/login")
def Account(request):
    return render(request, 'account/my-account.html')


def Home(request):
    try:
        brand = Brand.objects.all()
        category = Category.objects.all()

        sliders = Slider.objects.all().order_by('-id')[0:5]
        banner_areas = Banner_Area.objects.all().order_by('-id')[0:3]
        banner_bottom = Banner_Area.objects.all().order_by('-id')[3:5]

        top_deals_product = Product.objects.filter(section__name='Top Deals Of The Day')
        hot_deals = Product.objects.filter(section__name='Hot Deals')
        more_to_love = Product.objects.filter(section__name='More to love')

        compuer = Product.objects.filter(category__name='Computer Accessories').order_by('-id')[0:5]
        smart_phone = Product.objects.filter(category__name='Smart Phone').order_by('-id')[0:5]
        gadgets = Product.objects.filter(category__name='Gadget').order_by('-id')[0:5]
        women_fashion = Product.objects.filter(category__name='Beauty tools').order_by('-id')[0:5]
        skin_care = Product.objects.filter(category__name='Skin Care').order_by('-id')[1:5]

        top_skin_care = None
        skin_care_products = Product.objects.filter(category__name='Skin Care').order_by('-id')
        if skin_care_products.exists():
            top_skin_care = skin_care_products.first()

        top_bag = None
        top_bag_products = Product.objects.filter(category__name='Bags').order_by('-id')
        if top_bag_products.exists():
            top_bag = top_bag_products.first()

        top_beauty_tools = None
        Beauty_tools = Product.objects.filter(category__name='Beauty tools').order_by('-id')
        if Beauty_tools.exists():
            top_beauty_tools = Beauty_tools.first()

        top_shoes = None
        shoes = Product.objects.filter(category__name='Shoes').order_by('-id')
        if shoes.exists():
            top_shoes = shoes.first()

        top_muslim_wear = None
        muslim_wear = Product.objects.filter(category__name='Muslim Wear').order_by('-id')
        if muslim_wear.exists():
            top_muslim_wear = muslim_wear.first()

        context = {
            'brand': brand,
            'category': category,
            'sliders': sliders,
            'banner_areas' : banner_areas,
            'hot_deals': hot_deals,
            'top_deals_product': top_deals_product,
            'more_to_love': more_to_love,
            'compuer': compuer,
            'smart_phone': smart_phone,
            'gadgets': gadgets,
            'women_fashion' : women_fashion,
            'skin_care': skin_care,
            'top_skin_care': top_skin_care,
            'top_bag' : top_bag,
            'top_beauty_tools': top_beauty_tools,
            'top_shoes': top_shoes,
            'top_muslim_wear': top_muslim_wear,
            'banner_bottom': banner_bottom,
        }
        
        return render(request, 'main/home.html', context)
    except Exception as e:
        # Handle the exception here
        return redirect('404')



def ProductDetail(request, slug):
    # try:
    product = Product.objects.filter(slug=slug)

    for products in product:
        products.discounted_price_value = products.discounted_price()
        discount_price = products.discounted_price_value

    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')

    context = {
        'product': product,
        'discount_price': discount_price,
    }

    return render(request, "product/product_details.html", context)
    # except Exception as e:
    #     # Handle the exception here
    #     return HttpResponse('An error occurred while processing the request.')



def Register(request):
    try:
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
    except Exception as e:
        # Handle the exception here
        return redirect('404')
    

def Login(request):
    try:
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
    except Exception as e:
        # Handle the exception here
        return redirect('404')
    # return render(request, 'account/my-account.html')


def custom_logout(request):
    try:
        if request.method == 'POST':
            logout(request)
    except Exception as e:
        # Handle the exception here
        return redirect('404')  # Replace '404' with your desired redirect URL
    return redirect('home')  # Replace 'home' with your desired redirect URL



@login_required(login_url="/accounts/login")
def About(request):
    return render(request, 'main/about.html')

def Contact(request):
    return render(request, 'main/contact.html')





def Products(request):
    try:
        category = Category.objects.all()
        product = Product.objects.all()
        color = Color.objects.all()
        sizes = Product_Size.objects.all()
        brand = Brand.objects.all()

        for products in product:
            products.discounted_price_value = products.discounted_price()
            discount_price = products.discounted_price_value

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
            product = Product.objects.filter(price__lte=Int_FilterPrice)
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
    except Exception as e:
        # Handle the exception here
        return redirect('404')  # Replace '404' with your desired redirect URL






def filter_data(request):
    try:
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
    except Exception as e:
        # Handle the exception here
        return JsonResponse({'error': str(e)})





@login_required(login_url="/acounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    
    # Get the previous URL from the HTTP referer header
    previous_url = request.META.get('HTTP_REFERER')
    
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect('home')  # Fallback if no referer is found
    



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




@login_required(login_url="/accounts/login")
def cart_detail(request):
    cart = request.session.get('cart', {})
    
    coupon = None
    # valid_coupon = False
    # invalid_coupon = False
    coupon_discount = 0
    
    cart_count = sum(item['quantity'] for item in cart.values())
    cart_total_amount = sum(float(item['price']) * item['quantity'] for item in cart.values())
    
    context = {
        'coupon': coupon,
        'coupon_discount': coupon_discount,
        'cart_total_amount': cart_total_amount,
        'cart_count': cart_count,
    }

    return render(request, 'cart/cart.html', context)




@login_required(login_url="/accounts/login")
def checkout(request):
    coupon = None
    valid_coupon = False
    invalid_coupon = False
    coupon_discount = 0

    try:
        if request.method == "GET":
            coupon_code = request.GET.get('coupon_code')

            if coupon_code:
                try:
                    coupon = CuponCode.objects.get(code=coupon_code)
                    valid_coupon = True
                    coupon_discount = coupon.discount
                    messages.success(request, 'Coupon code applied successfully.')
                except CuponCode.DoesNotExist:
                    invalid_coupon = True
                    messages.error(request, 'Invalid coupon code.')
                except Exception as e:
                    messages.error(request, 'An error occurred while applying the coupon code.')
    except Exception as e:
        # Handle the exception here
        messages.error(request, 'An error occurred while processing the checkout.')

    context = {
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
        'coupon_discount': coupon_discount,
    }
    
    return render(request, 'cart/checkout.html', context)






@login_required
def checkoutOrder(request):
    try:
        if request.method == "POST":
            user = request.user
            product_name = request.POST.get('product_name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            company_name = request.POST.get('company_name')
            country = request.POST.get('country')
            address = request.POST.get('address')
            address_2 = request.POST.get('address_2')
            town_city = request.POST.get('town_city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            tranjection_number = request.POST.get('tranjection_number')
            tranjection_id = request.POST.get('tranjection_id')
            note = request.POST.get('note')
            cart_total_amount = request.POST.get('cart_total_amount')
            coupon_discount_price = request.POST.get('coupon_discount')
            shipping_cost = request.POST.get('shipping_cost')
            order_total = request.POST.get('order_total')

            orderCheckout = Checkout(
                user=user,
                product_name=product_name,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                country=country,
                address=address,
                address_2=address_2,
                town_city=town_city,
                state=state,
                postcode=postcode,
                phone=phone,
                email=email,
                tranjection_number=tranjection_number,
                tranjection_id=tranjection_id,
                note=note,
                cart_total_amount=cart_total_amount,
                coupon_discount_price=coupon_discount_price,
                shipping_cost=shipping_cost,
                order_total=order_total,
            )
            orderCheckout.save()
            cart_clear(request)
            # messages.success(request, 'Order placed successfully.')
        return redirect('home')
    except Exception as e:
        # Handle the exception here
        return redirect('404')  # Replace '404' with your desired redirect URL


def preOrder(request, id):
    product = Product.objects.get(id=id)


    context = {
        'product': product
    }
    return render(request, 'cart/preorder.html', context)


def SavePreOrder(request):
    if request.method == "POST":
        # user = request.user.email
        product_name = request.POST.get('product_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        country = request.POST.get('country')
        address = request.POST.get('address')
        address_2 = request.POST.get('address_2')
        town_city = request.POST.get('town_city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        tranjection_number = request.POST.get('tranjection_number')
        tranjection_id = request.POST.get('tranjection_id')
        note = request.POST.get('note')
        cart_total_amount = request.POST.get('cart_total_amount')
        coupon_discount_price = request.POST.get('coupon_discount')
        shipping_cost = request.POST.get('shipping_cost')
        order_total = request.POST.get('order_total')

        

        

        preorder = PreOrder(
            user=request.user.email,
            product_name=product_name,
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            country=country,
            address=address,
            address_2=address_2,
            town_city=town_city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            tranjection_number=tranjection_number,
            tranjection_id=tranjection_id,
            note=note,
            cart_total_amount=cart_total_amount,
            coupon_discount_price=coupon_discount_price,
            shipping_cost=shipping_cost,
            order_total=order_total,
        )
        preorder.save()
        # messages.success(request, 'Order placed successfully.')
    return redirect('home')




@login_required
def Order(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return redirect('login')  # or any other appropriate action

    checkout_obj = Checkout.objects.filter(user=user)

    context = {
        'checkout_obj': checkout_obj
    }

    return render(request, 'cart/order.html', context)
    # except Exception as e:
    #     return HttpResponse(f'{e}')
        # print(f"\n {e} \n")
        # Handle the exception here
        # return redirect('404')  # Replace '404' with your desired redirect URL
    


@login_required
def order_tracking(request):
    user = request.user
    checkouts = Checkout.objects.filter(user=user)

    if not checkouts.exists():
        # Handle the case when there are no checkouts for the user
        return redirect('cart_detail')  # Redirect to a default page or show a message

    context = {
        'checkouts': checkouts,
    }

    return render(request, 'cart/order_track.html', context)