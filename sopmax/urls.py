
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    # ERROR URL
    path('404', views.error404, name='404'),

    # path('admin/', include('admin_soft.urls')),
    path('admin/', admin.site.urls),
    path('base', views.base, name='base'),

    # HOME
    path('', views.Home, name='home'),
    path('about/', views.About, name='about-us'),
    path('contact/', views.Contact, name='contact-us'),
    path('product/', views.Products, name='product'),
    path('product/filter-data',views.filter_data,name="filter-data"),

    # PRODUCTS
    path("product/<slug:slug>", views.ProductDetail, name='product_detail'),


    # ACCOUNT
    path('account/myaccount', views.Account, name='myaccount'),
    path('account/register', views.Register, name='handleregister'),
    path('account/login', views.Login, name='handlelogin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', views.custom_logout, name='logout'),



    # CART
    path('cart/add/<uuid:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<uuid:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<uuid:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<uuid:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    # path('cart/save/',views.saveCart,name='save_cart'),

    # CHECKOUT
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/save/', views.checkoutOrder, name='savecheckout'),
    path('preorder/<uuid:id>', views.preOrder, name='preorder'),
    path('preorder/save', views.SavePreOrder, name='savepreorder'),
    path('order/', views.Order, name='order'),
    # path('order/tracking', views.OrderDetail, name='orderdetail'),

    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
