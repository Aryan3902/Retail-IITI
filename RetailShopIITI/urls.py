"""RetailShopIITI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from login import views
from shopapp.views import main_page, cart, main_page_product, main_page_cart_product, orders, main_page_order_product, main_page_electronics, main_page_stationary, main_page_household, main_page_fashion


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-in/', views.homeview),
    path('sign-in/signupauth/', views.signupauth),
    path('sign-in/login/', views.login),
    path('', views.welcome),
    path('home/', views.openview),
    path('resetpassword/', views.forgetview),
    path('ticket/', views.ticket, name='ticket'),
    path('main-page/', main_page),
    path('main-page/electronics/', main_page_electronics),
    path('main-page/stationary/', main_page_stationary),
    path('main-page/household/', main_page_household),
    path('main-page/fashion/', main_page_fashion),
    path('main-page/<int:id>/', main_page_product),
    path('main-page/cart/<int:id>/', main_page_cart_product),
    path('main-page/orders/<int:id>/', main_page_order_product),
    path('main-page/cart/', cart),
    path('main-page/orders/', orders)
]
