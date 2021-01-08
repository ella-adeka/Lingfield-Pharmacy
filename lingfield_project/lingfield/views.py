from django.shortcuts import render
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# from .forms import UserInfoForm, UserAddressForm
# from .models import UserInfo, UserAddress

# from accounts.forms import UserRegisterForm, UserProfileForm, UpdateForm
# from accounts.models import UserProfile

from operator import attrgetter
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'lingfield/index.html')

def about(request):
    return render(request, 'lingfield/about.html')


def blog(request):
    return render(request, 'lingfield/blog.html')

def branches(request):
    return render(request, 'lingfield/branches.html')


def complaints(request):
    return render(request, 'lingfield/complaints.html')

def contact(request):
    return render(request, 'lingfield/contact.html')

def download(request):
    return render(request, 'lingfield/download.html')

def head_office(request):
    return render(request, 'lingfield/head_office.html')

def footer(request):
    return render(request, 'lingfield/footer.html')


def leaflets(request):
    return render(request, 'lingfield/leaflets.html')



def prescriptions(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect('accounts:dashboard')
    # else:
    #     return login(request)
    return render(request, 'lingfield/prescriptions.html')

def register(request):
    return render(request, 'lingfield/register.html')


def services(request):
    return render(request, 'lingfield/services.html')

def settings(request):
    return render(request, 'lingfield/settings.html')


