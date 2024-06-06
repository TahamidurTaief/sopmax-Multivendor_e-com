from .models import Checkout, Main_Category, Sub_Category, Category


def cart_item_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return {
        'cart_count': cart_count
    }


def order_count(request):
    if request.user.is_authenticated:
        total_orders = Checkout.objects.filter(user=request.user).count()
    else:
        total_orders = 0
    
    return {'total_orders': total_orders}



def categories(request):
    main_cat = Main_Category.objects.all()
    sub_cat = Sub_Category.objects.all()
    cat = Category.objects.all()

    return {
        'main_cat': main_cat,
        'sub_cat': sub_cat,
        'cat': cat,
    }