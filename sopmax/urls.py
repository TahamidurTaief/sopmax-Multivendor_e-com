
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

    # PRODUCTS
    path("product/<slug:slug>", views.ProductDetail, name='product_detail'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
