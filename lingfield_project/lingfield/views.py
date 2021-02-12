from django.shortcuts import render
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from operator import attrgetter
from django.contrib import messages
# Create your views here.

# ADMIN
# The 404 (page not found) view¶
def handler404(request, exception, template_name='admin/404.html'):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

def handler500(request, exception, template_name='admin/500.html'):
    response = render_to_response(template_name)
    response.status_code = 500
    return response

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
    return render(request, 'lingfield/prescriptions.html')

def register(request):
    return render(request, 'lingfield/register.html')


def services(request):
    return render(request, 'lingfield/services.html')

def settings(request):
    return render(request, 'lingfield/settings.html')


