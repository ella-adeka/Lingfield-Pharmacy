from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import *
from .models import *

from medicines.models import Medicine

from operator import attrgetter
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
    medicine_form_class = MedicineItemsForm
    template_name = "registration/dashboard.html"

    def get_queryset(self):
        return MedicineItems.objects.filter(owner=self.kwargs['pk'])

    def get(self,request,*args,**kwargs):
        try:
            u_form = self.u_form_class(instance=request.user,prefix='info')
            b_form = self.b_form_class(instance=request.user.userbirthdate, prefix='info')
            p_form = self.p_form_class(instance=request.user.userprofile, prefix='info')
            surgery_form = self.surgery_form_class(instance=request.user.addsurgery, prefix='addsurgery')
            dependent_form = self.dependent_form_class(instance=request.user.dependent,prefix='dependent')
            medicine_form = self.medicine_form_class(instance=request.user,prefix='medicineitems')
            hospital_list = HospitalList.objects.all() 
            saved_surgery = AddSurgery.objects.filter(user=request.user,saved=False)
            medicines = Medicine.objects.all()
            medicine_items = MedicineItems.objects.filter(user=request.user, added=False) #[::-1]
            selected_surgeries = SelectSurgery.objects.filter(user=request.user, added=False)
            prescription = PrescriptionItem.objects.filter(user=self.request.user, ordered=False)
            context = {
                'u_form': u_form,
                'b_form': b_form,
                'p_form': p_form,
                'surgery_form' : surgery_form,
                'saved_surgery' : saved_surgery,
                'dependent_form' : dependent_form,
                'medicine_form' : medicine_form,
                'hospital_list' : hospital_list,
                'medicines' : medicines,
                'medicine_items' : medicine_items,
                'selected_surgeries' :selected_surgeries,
                'prescription' : prescription,
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
                saved_surgery = surgery_form.cleaned_data.get('surgery_name')
                saved_surgery.save()
                print(saved_surgery)
                messages.info(request,  f'Your information has been added successful!')
                context = {
                    'saved_surgery' : saved_surgery,
                }
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formThree':
            medicine_form = MedicineItemsForm(request.POST, prefix='medicineitems')
            if medicine_form.is_valid():
                item = medicine_form.cleaned_data.get('item')
                quantity = medicine_form.cleaned_data.get('quantity')
                reminder = medicine_form.cleaned_data.get('reminder')
                medicine_item, created = MedicineItems.objects.get_or_create(
                    user=request.user,
                    item=item,
                    quantity=quantity,
                    reminder=reminder,
                    added=False,
                )
                medicine_item.save()
                if medicine_item == 'None':
                    medicine_item.delete()
                if medicine_item == None:
                    medicine_item.delete()
                # for med in medicine_item[2:]:
                #     med.delete()
                #     messages.info(request,  f'Delete previously selected item!')
                #     return redirect('accounts:dashboard')
                # med_item = medicine_item[len(medicine_item)]
                # if medicine_item.count() == 1:
                #     medicine_item.save()
                # else:
                #     messages.info(request,  f'Delete previously selected item!')
                #     return redirect('accounts:dashboard')
                
                # if  medicine_item:
                #     medicine_item.delete()
                #     messages.info(request,  f'Could not save item. Delete preselected item before adding a new one!')
                #     return redirect('accounts:dashboard')
                # else: 
                #     medicine_item.save()
                   
                # if medicine_item == 1 :
                #     medicine_item.save()
                # else: 
                #     medicine_item.delete()
                #     messages.info(request,  f'Cannot save item!')
                #     return redirect('accounts:dashboard')
                messages.info(request,  f'Item saved!')
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formFour':
            dependent_form = DependentForm(request.POST,instance=request.user.dependent, prefix='dependent')
            if dependent_form.is_valid():
                dependent_form.save()
                messages.info(request,  f'Dependent details updated!')
                return redirect('accounts:dashboard')
        context = {
            'u_form': u_form,
            'b_form': b_form,
            'p_form': p_form,
            'surgery_form' : surgery_form,
            'dependent_form' : dependent_form,
            'saved_surgery' : saved_surgery,
            'selected_surgeries' :selected_surgeries,
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

@receiver(post_save, sender=User, dispatch_uid='save_medicine')
def save_medicine_item(sender, instance, created, **kwargs):
    user = instance
    if created:
        medicine_item = MedicineItems(user=user)
        medicine_item.save()


global surgery
def surgery(request,slug):
    try:
        surgery=None
        surgery = get_object_or_404(HospitalList, slug=slug)
        the_surgery, created = SelectSurgery.objects.get_or_create(
            user=request.user,
            surgery=surgery,
            added=False,
        )
        surgery_qs=SelectSurgery.objects.filter(user=request.user, added=False)
        surgery.save()
        print(surgery)
        messages.info(request, "Your surgery has been selected!")
        return redirect('accounts:dashboard')
    except ObjectDoesNotExist:
        messages.warning(self.request,"Surgery Does Not Exist!")
        return redirect("accounts:dashboard")

# orders = Order.objects.filter(customer=customer, complete=False)

# if not orders.exists():
#     order = Order.objects.create(customer=customer, complete=False)
# else:
#     order = orders.last()


def delete_medicine(request, id):
    item = get_object_or_404(MedicineItems, id=id)
    item.delete()
    messages.info(request, "Item was deleted.")
    return redirect("accounts:dashboard")

def delete_prescription(request, id):
    pres_item = get_object_or_404(PrescriptionItem, id=id)
    pres_item.delete()
    messages.info(request, "PrescriptionItem was deleted.")
    return redirect("accounts:dashboard")


def new_prescription(request):
    try:
        selected_surgery = get_object_or_404(SelectSurgery, user=request.user, added=False) #objects.select_related().filter(programme = programme_id)
        # medicine_item = MedicineItems.objects.select_related().filter( user=request.user, added=False)
        medicine_item = MedicineItems.objects.filter(user=request.user, added=False)[0]
        # medicine_item = MedicineItems.objects.get(user=request.user, added=False)
        prescription_item = PrescriptionItem.objects.create(
            user=request.user,
            selected_surgery=selected_surgery,
            medicine_item=medicine_item,
            ordered=False
        )
        prescription_qs = Prescription.objects.filter(user=request.user, complete=False)
        prescription_item.save()
        print(selected_surgery)
        print(medicine_item)
        messages.success(request,"Prescription Created!")
    except ObjectDoesNotExist:
        messages.warning(request,"Prescription Not Created!")
        return redirect("accounts:dashboard")
    # except MultipleObjectsReturned:
    #     medicine_item = MedicineItems.objects.filter(user=request.user, added=False)
    #     print(medicine_item)
    #     messages.warning(request,"Prescription Not Created!")
    #     return redirect("accounts:dashboard")
    except ValueError:
        print(selected_surgery)
        print(medicine_item)
        messages.warning(request,"Cannot assign 'QuerySet [<MedicineItems: item>]': 'PrescriptionItem.medicine_item' must be a 'MedicineItems' instance.!")
        return redirect("accounts:dashboard")
    return redirect("accounts:dashboard")