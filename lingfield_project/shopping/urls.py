"""lingfield_project URL Configuration

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
from shopping import views
from .views import ShopDetailView, ShopListView, SearchResultsView, CartView, CheckOutView

app_name="shopping"

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('delivery/', views.delivery, name='delivery'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:subcategory_slug>/', views.product_list, name='product-list-by-subcategory'),
    path('product-detail/<slug:slug>/', ShopDetailView.as_view(), name='product_detail'),

    path('search-result/', SearchResultsView.as_view(), name='search'),

    path('products/add_to_cart/<slug>', views.add_to_cart, name='add_to_cart'),
    path('products/remove_from_cart/<slug>', views.remove_from_cart, name='remove_from_cart'),
    path('products/remove_single_item_from_cart/<slug>', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
]