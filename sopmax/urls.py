
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
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
