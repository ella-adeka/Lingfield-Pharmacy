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
from health_advice import views
from .models import HealthAdvice
from .views import HealthAdviceDetailView, HealthAdviceListView, SearchResultsView, CategoryDetailView

app_name="health_advice"

urlpatterns = [
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='health-advice-category-detail'),
    path('category/', views.health_advice_category_list, name='health-advice-category-list'),
    
    path('category/detail/<slug:slug>/', HealthAdviceDetailView.as_view(),  name='health-advice-detail'),
    
    path('search/', SearchResultsView.as_view(), name="search"),
]