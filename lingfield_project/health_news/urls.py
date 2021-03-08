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
from health_news import views
from .views import  SearchResultsView, HealthNewsDayArchiveView

app_name="health_news"

urlpatterns = [
    # List views
    path('news-list/', views.health_news_list, name='health-news-list'),
    path('<slug:category_slug>/', views.health_news_list, name='health-news-list-by-category'),

    # Detail View
    path('news-detail/<int:id>/', views.health_news_detail, name='health-news-detail'),
    
    # Search View
    path('search-result/', SearchResultsView.as_view(), name="search"),

    path('<int:year>/<str:month>/<int:day>/', HealthNewsDayArchiveView.as_view(), name="health_news_day"),

]   