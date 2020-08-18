
"""foodorder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static

import home
from foodorder import settings
from home import views
from order import views as OrderViews
from user import views as UserViews




urlpatterns = [

    path('home/', views.index, name='home'),
    path('', views.index, name='home'),
    path('about/', views.aboutus, name='about'),
    path('order/', include('order.urls')),
    path('contact/', views.contactus, name='contact'),
    path('home/about/', views.aboutus, name='about'),
    path('search/', views.search, name='search'),
    path('auto_search/', views.search, name='auto_search'),
    path('home/contact/', views.contactus, name='contact'),
    path('product/', include('product.urls')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('login/', UserViews.login_form, name='login_form'),
    path('logout/', UserViews.logout_fuc, name='logout_ffunc'),
    path('signup/', UserViews.signup_form, name='signup_form'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
