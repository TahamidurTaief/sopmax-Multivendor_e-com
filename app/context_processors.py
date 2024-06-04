
def cart_item_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return {
        'cart_count': cart_count
    }



from .models import Main_Category, Sub_Category, Category

def categories(request):
    main_cat = Main_Category.objects.all()
    sub_cat = Sub_Category.objects.all()
    cat = Category.objects.all()

    return {
        'main_cat': main_cat,
        'sub_cat': sub_cat,
        'cat': cat,
    }