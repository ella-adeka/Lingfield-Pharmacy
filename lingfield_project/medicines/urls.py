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
from django.shortcuts import reverse
from django.conf.urls import url
from medicines import views
from .views import MedicineDetailView, MedicineListView, SearchResultsView, CategoryDetailView

app_name="medicines"

urlpatterns = [
    path('medicine-category-detail/<slug:slug>/', CategoryDetailView.as_view(), name='medicine-category-detail'),
    path('medicine-category-list/', views.medicine_category_list, name='medicine-category-list'),
    
    path('medicine-detail/<slug:slug>/', MedicineDetailView.as_view(), name='medicine-detail'),
    path('medicine-list/<slug:slug>/', MedicineListView.as_view(), name='medicine-list'),

    path('search/', SearchResultsView.as_view(), name="search"),
]