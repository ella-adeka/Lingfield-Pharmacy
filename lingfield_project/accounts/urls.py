from django.urls import path,include, re_path
from . import views
from .views import DashboardView
from django.contrib.auth import views as auth_views

app_name = "accounts"
# Create you views here
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('signup/',views.signup, name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path('dashboard/select_surgery/<int:id>/',views.select_surgery, name='select_surgery')
    path('dashboard/select_surgery/<slug:slug>/', DashboardView.as_view(), name="dashboard-with-surgery"),
    # path('dashboard/select_surgery/<slug:slug>', views.select_surgery, name="select_surgery"),
    path('dashboard/new_prescription/', views.new_prescription, name="new_prescription"),
    path('dashboard/new_prescription/<slug:hospital_slug>/', views.new_prescription, name="new_prescription_with_hospital"),
    path('dashboard/new_prescription/<slug:medicine_slug>/', views.new_prescription, name="new_prescription_with_meds")
]

