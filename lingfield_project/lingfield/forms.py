from django import forms
from crispy_forms.helper import FormHelper
from accounts.forms import UserRegisterForm, UserProfileForm, UpdateForm
from .models import UserInfo, UserAddress
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
    get_user_model

)

#create your forms here
