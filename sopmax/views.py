from django.shortcuts import redirect, render
from app.models import *



# Create your views here.
def base(request):
    return render(request, 'base.html')

def error404(request):
    return render(request, 'error/404.html')


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