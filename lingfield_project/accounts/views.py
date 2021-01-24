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
    medicineitems_form_class = MedicineItemsForm
    template_name = "registration/dashboard.html"

    def get(self,request,*args,**kwargs):
        try:
            u_form = self.u_form_class(instance=request.user,prefix='info')
            b_form = self.b_form_class(instance=request.user.userbirthdate, prefix='info')
            p_form = self.p_form_class(instance=request.user.userprofile, prefix='info')
            surgery_form = self.surgery_form_class(instance=request.user.addsurgery, prefix='addsurgery')
            dependent_form = self.dependent_form_class(instance=request.user.dependent,prefix='dependent')
            medicineitems_form = self.medicineitems_form_class(instance=request.user,prefix='medicineitems')
            hospital_list = HospitalList.objects.all() 
            saved_surgery = AddSurgery.objects.filter(user=request.user)
            medicines = Medicine.objects.all()
            medicine_items = MedicineItems.objects.filter(user=request.user, added=False)
            selected_surgeries = SelectSurgery.objects.filter(user=request.user, added=False)
            context = {
                'u_form': u_form,
                'b_form': b_form,
                'p_form': p_form,
                'surgery_form' : surgery_form,
                'saved_surgery' : saved_surgery,
                'dependent_form' : dependent_form,
                'medicineitems_form' : medicineitems_form,
                'hospital_list' : hospital_list,
                'medicines' : medicines,
                'medicine_items' : medicine_items,
                'selected_surgeries' :selected_surgeries,
            }
            return render(self.request, "registration/dashboard.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"No information available here!")
            return redirect("accounts:dashboard")


    def post(self, request,slug=None, *args, **kwargs):  
      
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
                messages.info(request,  f'Dependent details updated!')
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formFour':
            medicineitems_form = MedicineItemsForm(request.POST,instance=request.user, prefix='medicineitems')
            if medicineitems_form.is_valid():
                medicine_items = medicineitems_form.cleaned_data['item']
                medicineitems_form.save()
                messages.info(request,  f'Item saved!')
                print(medicine_items)
                context = {
                    'medicine_items' : medicine_items,
                }
                return redirect('accounts:dashboard')
        context = {
            'u_form': u_form,
            'b_form': b_form,
            'p_form': p_form,
            'surgery_form' : surgery_form,
            'dependent_form' : dependent_form,
            'medicineitems_form' : medicineitems_form,
            'saved_surgery' : saved_surgery,
            'selected_surgeries' :selected_surgeries,
            'medicine_items' : medicine_items,
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


# @receiver(post_save, sender=User, dispatch_uid='save_medicine')
# def save_medicine_item(sender, instance, created, **kwargs):
#     user = instance
#     if created:
#         item = MedicineItems(user=user)
#         item.save()

@receiver(post_save, sender=User, dispatch_uid='save_medicine')
def save_medicine_item(sender, instance, created, **kwargs):
    user = instance
    if created:
        saved_medicine_items = MedicineItems(user=user)
        saved_medicine_items.save()



global surgery
def surgery(request,slug):
    try:
        surgery=None
        surgery = get_object_or_404(HospitalList, slug=slug)
        the_surgery, created = SelectSurgery.objects.get_or_create(
            user=request.user,
            surgery=surgery,
            added=False,
            # surgery__slug=surgery.slug,
        )
        surgery_qs=SelectSurgery.objects.filter(user=request.user, added=False)
        # if surgery_qs.exists():
        #     the_surgery.save(update_fields=['surgery'])
        # else:
        #     the_surgery.save()
        # if the_surgery.exists():
        #     the_surgery.delete()
        # else:
        surgery.save()
        # the_surgery.delete()
        print(surgery)
        messages.info(request, "Your surgery has been selected!")
        return redirect('accounts:dashboard')
    except ObjectDoesNotExist:
        messages.warning(self.request,"Surgery Does Not Exist!")
        return redirect("accounts:dashboard")

global item
def item(request,slug):
    item=None
    item = get_object_or_404(Medicine, slug=slug)
    the_item, created = MedicineItems.objects.get_or_create(
        user=request.user,
        item=item,
        added=False,
    )
    the_item.save()
    messages.info(request, "Your item has been added!")
    # print(the_item)
    # print(item)
    # print(quantity)
    return redirect('accounts:dashboard')

# def register(request):
#     if request.method=='POST':
#         form=UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/accounts')

#     else:
#         form=UserCreationForm()
#         args={'form':form}
#         return render(request,'accounts/reg_form.html',args)  

def new_prescription(request):
    try:
        selected_surgeries = SelectSurgery.objects.filter(user=request.user, added=False)
        # selected_surgeries = SelectSurgery.objects.get(user=request.user, added=False)
    except ObjectDoesNotExist:
        messages.warning(request,"Prescription Not Created!")
        return redirect("accounts:dashboard")
    return redirect("accounts:dashboard")
    # medicineitem = get_object_or_404(MedicineItems, slug=slug)
    # print(surgery)
    # prescription_item, created = PrescriptionItem.objects.get_or_create(
    #     user=request.user,
    #     surgery=surgery,
    #     id=id,
    #     # medicineitem=medicineitem,
    # )
    # prescription_qs = Prescription.objects.filter(user=request.user, ordered=False)
    # return redirect('accounts:dashboard')


# def new_prescription(request):
#     the_surgery = get_object_or_404(HospitalList)
#     # medicineitem = get_object_or_404(MedicineItems, slug=slug)
#     print(surgery)
#     prescription_item, created = PrescriptionItem.objects.get_or_create(
#         user=request.user,
#         surgery=surgery,
#         # medicineitem=medicineitem,
#     )
#     prescription_qs = Prescription.objects.filter(user=request.user, ordered=False)
#     if prescription_qs.exists():
#         prescription = prescription_qs[0]
#         # check if the prescription item is in the prescription
#         if prescription.items.filter().exists():
#             prescription_item.item_quantity += 1
#             prescription_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("shopping:cart")
#         else:
#             prescription.items.add(prescription_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("shopping:cart")
#     else:
#         date_ordered = timezone.now()
#         prescription = prescription.objects.create(
#             user=request.user, date_ordered=date_ordered)
#         prescription.items.add(prescription_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("shopping:cart")
#     # p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
#     return redirect('accounts:dashboard')


