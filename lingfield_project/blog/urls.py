from django.urls import path,include
from . import views


app_name = "blog"
# Create you views here
urlpatterns = [
    path('blog_list/',views.blog_list, name="blog_list"),
   
]

