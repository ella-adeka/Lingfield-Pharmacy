from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView,  TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .forms import *
from .models import *

from medicines.models import Medicine

from operator import attrgetter
from django.contrib import messages
# from lingfield.views import get_item_queryset
from django.contrib import messages
from django.core.mail import send_mail


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    u_form_class = UpdateForm
    b_form_class = UserBirthDateForm
    p_form_class = UserProfileForm
    surgery_form_class = AddSurgeryForm
    dependent_form_class = DependentForm
    template_name = "registration/dashboard.html"

    def get_context_data(self,slug,*args,**kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        context['select_surgery'] = HospitalList.objects.all 
        # context['select_surgery'] = HospitalList.objects.filter(user=request.user,slug=slug)  
        # context['hospital'] = get_object_or_404(HospitalList, user=request.user, slug=slug)  
        return context

    def get(self,request,*args,**kwargs):
        try:
            u_form = self.u_form_class(instance=request.user,prefix='info')
            b_form = self.b_form_class(instance=request.user.userbirthdate, prefix='info')
            p_form = self.p_form_class(instance=request.user.userprofile, prefix='info')
            surgery_form = self.surgery_form_class(instance=request.user.addsurgery, prefix='addsurgery')
            dependent_form = self.dependent_form_class(instance=request.user.dependent,prefix='dependent')
            hospital_list = HospitalList.objects.all() 
            saved_surgery = AddSurgery.objects.all()
            medicines = Medicine.objects.all()
            
            context = {
                'u_form': u_form,
                'b_form': b_form,
                'p_form': p_form,
                'surgery_form' : surgery_form,
                'saved_surgery' : saved_surgery,
                'dependent_form' : dependent_form,
                'hospital_list' : hospital_list,
                'medicines' : medicines,
                
            }
            return render(self.request, "registration/dashboard.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"No information available here!")
            return redirect("accounts:dashboard")

        try:
            prescription = Prescription.objects.get(user=self.request.user, ordered=False)
            context = {
                'prescription' : prescription,
            }
            return render(self.request, "registration/dashboard.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have an active order.")
            return redirect("accounts:dashboard")

    def post(self, request,slug, *args, **kwargs):
        try:
            prescription = Prescription.objects.get(user=self.request.user, ordered=False)
            return redirect("accounts:dashboard")
        except ObjectDoesNotExist:
            messages.info("You do not have an active order.")
            return redirect("accounts:dashboard")
        

        if request.POST.get("form_type") == 'formOne':  
            u_form = UpdateForm(request.POST,instance=request.user, prefix='info')
            b_form = UserBirthDateForm(request.POST, request.FILES, instance=request.user.userbirthdate, prefix='info')
            p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile, prefix='info')
            if u_form.is_valid() and b_form.is_valid() and p_form.is_valid():
                u_form.save()
                b_form.save()
                p_form.save()
                messages.info(request,  f'Your information has been updated!')
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formTwo':
            surgery_form = AddSurgeryForm(request.POST, prefix='addsurgery')
            if surgery_form.is_valid():
                saved_surgery = surgery_form.cleaned_data['surgery_name']
                surgery_form.save()
                messages.info(request,  f'Your information has been added successful!')
                context = {
                    'saved_surgery' : saved_surgery,
                }
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formThree':
            dependent_form = DependentForm(request.POST,instance=request.user.dependent, prefix='dependent')
            if dependent_form.is_valid():
                dependent_form.save()
                messages.info(request,  f'Dependent datails updated!')
                return redirect('accounts:dashboard')
        context = {
            'u_form': u_form,
            'b_form': b_form,
            'p_form': p_form,
            'surgery_form' : surgery_form,
            'dependent_form' : dependent_form,
            'saved_surgery' : saved_surgery,
        }
        return render(request, self.template_name,context)
                
def signup(request):
    context = {}
    form = UserRegisterForm(request.POST or None)
    birth_form = UserBirthDateForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid() and  birth_form.is_valid():
            user = form.save()
            user.save()
            birth = birth_form.save(commit=False)
            birth.user = user
            login(request,user)
            # return reverse_lazy('login')
            return render(request,'lingfield/index.html')
        else:
            print(form.errors,birth_form.errors)
    else:
        form = UserRegisterForm()
        birth_form = UserBirthDateForm()
    return render(request, 'registration/signup.html',{'form':form,'birth_form':birth_form,})

def new_prescription(request, medicine_slug=None, hospital_slug=None):
    # hospital = ""
    # medicine = ""
    # hospital = []
    hospital = get_object_or_404(HospitalList, slug=hospital_slug)
    medicine = get_object_or_404(Medicine, medicine_slug=medicine_slug)
    prescription_item, create = PrescriptionItem.objects.create(
        user=request.user,
        hospital=hospital,
        medicine=medicine,
        ordered=False,
    )
    prescription_qs = Prescription.objects.create(user=request.user, ordered=False)
    if prescription_qs.exists():
        prescription = prescription_qs[0]
        # check if the prescription item is in the prescription
        if prescription.items.filter(medicine__slug=medicine.slug,hospital__slug=hospital.slug).exists():
            prescription_item.prescription_quantity += 1
            prescription_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("accounts:dashboard")
        else:
            prescription.items.add(prescription_item)
            messages.info(request, "This item was added to your prescription.")
            return redirect("accounts:dashboard")
    else:
        date_ordered = timezone.now()
        prescription = Prescription.objects.create(
            user=request.user, date_ordered=date_ordered)
        prescription.items.add(prescription_item)
        messages.info(request, "This item was added to your prescription.")
    return redirect('accounts:dashboard')

def select_surgery(request, slug):
    hospital = get_object_or_404(HospitalList, user=request.user, slug=slug)  
    return redirect('accounts:dashboard')


# def select_surgery(request, slug):
#     hospital = HospitalList.objects.filter(user=request.user, slug=slug)
#     selected_surgery = HospitalList.objects.filter(slug=slug)
#     if hospital.exists():
#         prescription_item.update(hospital)
#         messages.info(request, "{} was updated to your prescription.".format(self.hospital))
#         return redirect("accounts:dashboard")
#     else:
#         prescription_item.add(hospital)
#         messages.info(request, "{} was added to your prescription.".format(self.hospital))
#         return redirect("accounts:dashboard")
#     return redirect('accounts:dashboard')




# def select_surgery(request, slug):
#     hospital = get_object_or_404(HospitalList, slug=slug)
#     # selected_surgery = HospitalList.objects.filter(slug=slug)
#     prescription_item, create = PrescriptionItem.objects.create(
#         user=request.user,
#         hospital=hospital,
#         ordered=False,
#     )
#     prescription_qs = Prescription.objects.create(user=request.user, ordered=False)
#     if prescription_qs.exists():
#         if prescription.items.filter(hospital_id=hospital.id):
#             prescription.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("accounts:dashboard")
#         else:
#             prescription.items.add(prescription_item)
#             messages.info(request, "This item was added to your prescription.")
#             return redirect("accounts:dashboard")
#     else:
#         date_ordered = timezone.now()
#         prescription = Prescription.objects.create(
#             user=request.user, date_ordered=date_ordered)
#         prescription.items.add(prescription_item)
#         messages.info(request, "This item was added to your prescription.")
#     return redirect('accounts:dashboard')


    

@receiver(post_save, sender=User, dispatch_uid='save_new_user_birthdate')
def save_birthdate(sender, instance, created, **kwargs):
    user = instance
    if created:
        birthdate = UserBirthDate(user=user)
        birthdate.save()


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()
    
@receiver(post_save, sender=User, dispatch_uid='save_new_user_dependent')
def save_dependent(sender, instance, created, **kwargs):
    user = instance
    if created:
        dependent = Dependent(user=user)
        dependent.save()
     
@receiver(post_save, sender=User, dispatch_uid='save_new_surgery')
def save_surgery(sender, instance, created, **kwargs):
    user = instance
    if created:
        surgery = AddSurgery(user=user)
        surgery.save()

