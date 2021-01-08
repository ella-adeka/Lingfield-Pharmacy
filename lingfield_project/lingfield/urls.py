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
from health_news.views import health_news_detail


from lingfield import views

app_name="lingfield"

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('branches/', views.branches, name='branches'),
    path('complaints/', views.complaints, name='complaints'),
    path('contact/', views.contact, name='contact'),
    path('download/', views.download, name='download'),
    path('head-office/', views.head_office, name='head_office'),
    path('leaflets/', views.leaflets, name='leaflets'),
    path('more-info/', views.footer, name='more-info'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('settings/', views.settings, name='settings'),
    path('services/', views.services, name='services'),

   
]


