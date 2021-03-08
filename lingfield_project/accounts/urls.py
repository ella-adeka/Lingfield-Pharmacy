from django.urls import path,include, re_path
from . import views
from .views import DashboardView
from django.contrib.auth import views as auth_views

app_name = "accounts"
# Create you views here
urlpatterns = [
    # Dashboard Views.
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('dashboard/<int:id>/', DashboardView.as_view(), name="dashboard"),

    # User Authentication.
    path('signup/',views.signup, name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # For selecting surgery.
    path('dashboard/hospital/<slug:slug>/', DashboardView.as_view(), name="dashboard-with-surgery"),
    path('dashboard/surgery/<slug:slug>/', views.surgery, name="surgery"),

    # Delete urls.
    path('dashboard/delete/medicine-item/<int:id>/', views.delete_medicine, name="delete_medicine"),
    path('dashboard/delete/prescription-item/<int:id>/', views.delete_prescription_item, name="delete_prescription_item"),
    path('dashboard/delete/prescription/<int:id>/', views.delete_prescription, name="delete_prescription"),

    # For creating new precriptions.
    path('dashboard/new_prescription//', views.new_prescription, name="new_prescription"),
    path('dashboard/new_prescription/<int:id>/', views.new_prescription, name="new_prescription"),


]

