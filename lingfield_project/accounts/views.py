from django.shortcuts import render,redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View, ListView, DetailView, TemplateView, FormView

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import *
from .models import *
from medicines.models import Medicine

from operator import attrgetter
from django.contrib import messages
from django.core.mail import send_mail


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver



# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    # form_class: Form handling in class-based views.
    u_form_class = UpdateForm
    b_form_class = UserBirthDateForm
    p_form_class = UserProfileForm
    surgery_form_class = AddSurgeryForm
    dependent_form_class = DependentForm
    medicine_form_class = MedicineItemsForm
    order_form_class = OrderForm
    template_name = "registration/dashboard.html"


    def get(self,request,*args,**kwargs):
        try:
            u_form = self.u_form_class(instance=request.user,prefix='info')
            b_form = self.b_form_class(instance=request.user.userbirthdate, prefix='info')
            p_form = self.p_form_class(instance=request.user.userprofile, prefix='info')
            surgery_form = self.surgery_form_class(instance=request.user, prefix='addsurgery')
            dependent_form = self.dependent_form_class(instance=request.user.dependent,prefix='dependent')
            medicine_form = self.medicine_form_class(instance=request.user,prefix='medicineitems')
            order_form = self.order_form_class(instance=request.user,prefix='prescription')
            hospital_list = HospitalList.objects.all() 
            saved_surgery = AddSurgery.objects.filter(user=request.user)
            medicines = Medicine.objects.all()
            med_items = MedicineItems.objects.filter(user=request.user, added=False)
            selected_surgeries = SelectSurgery.objects.filter(user=request.user, added=True)
            prescription_item = PrescriptionItem.objects.filter(user=request.user, ordered=False)
            prescription = Prescription.objects.filter(user=self.request.user, ordered=True)
            context = {
                'u_form': u_form,
                'b_form': b_form,
                'p_form': p_form,
                'surgery_form' : surgery_form,
                'saved_surgery' : saved_surgery,
                'dependent_form' : dependent_form,
                'medicine_form' : medicine_form,
                'order_form' : order_form,
                'hospital_list' : hospital_list,
                'medicines' : medicines,
                'med_items' : med_items,
                'selected_surgeries' :selected_surgeries,
                'prescription_item' : prescription_item,
                'prescription' : prescription
            }
            return render(self.request, "registration/dashboard.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"No information available here!")
            return redirect("accounts:dashboard")


    def post(self, request,id=id, slug=None, *args, **kwargs):
        # form_type is used to specify which form is being saved at the moment. Using it will save each information to its respected form without affeting all the forms.  
        # form_type is added as a name on an input field in a form
        
        if request.POST.get("form_type") == 'formOne': 
            # All three forms are for updating the user's info 
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
            # This form is for adding more hospitals for the surgery
            surgery_form = AddSurgeryForm(request.POST, prefix='addsurgery')
            if surgery_form.is_valid():
                saved_surgery = surgery_form.cleaned_data.get('surgery_name')
                surgery_form.save()
                print(saved_surgery)
                messages.info(request,  f'Your information has been added successful!')
                context = {
                    'saved_surgery' : saved_surgery,
                }
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formThree':
            # Form for selecting the quantity of medicine for the prescription.
            medicine_form = MedicineItemsForm(request.POST, prefix='medicineitems')
            if medicine_form.is_valid():
                # item is gotten from the Medicine Model in medicine.models.
                item = medicine_form.cleaned_data.get('item')
                quantity = medicine_form.cleaned_data.get('quantity')
                reminder = medicine_form.cleaned_data.get('reminder')
                medicine_item = MedicineItems.objects.create(
                    user=request.user,
                    item=item,
                    quantity=quantity,
                    reminder=reminder,
                    added=False
                )
                messages.info(request,  f'Item saved!')
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formFour':
            dependent_form = DependentForm(request.POST,instance=request.user.dependent, prefix='dependent')
            if dependent_form.is_valid():
                dependent_form.save()
                messages.info(request,  f'Dependent details updated!')
                return redirect('accounts:dashboard')
        elif request.POST.get("form_type") == 'formFive':
            # Form for confirming prescription order
            order_form = OrderForm(request.POST, prefix='prescription')
            if order_form.is_valid():
                # All three instances (receival, prescription_note, and deleivery_note) are optional fields(as stated in accounts.forms.py).
                receival = order_form.cleaned_data.get('receival')
                prescription_note = order_form.cleaned_data.get('prescription_note')
                delivery_note = order_form.cleaned_data.get('delivery_note')
                # Prescription is created with the three instances above(excluding items, which is a ManyToManyField)
                # items is already created and saved at this stage(in PrescriptionItem).
                # Hence, it will just be added to Prescription with the .add() method.
                # items is a ManyToManyField because each item created should have an id, and this can be created automatically with ManyToManyField and no ForeignKey.
                prescription = Prescription.objects.create(
                    user=request.user,
                    receival=receival,
                    prescription_note=prescription_note,
                    delivery_note=delivery_note,
                    ordered=True
                ) 

                # Since the number of PrescriptionItems to be created cannot be estimated/known
                # A for loop is used, each item in PrescriptionItem will be added to Prescription, once a Precription is confirmed.
                # Add each PrescriptionItem object set to ordered=False
                for item in PrescriptionItem.objects.filter(user=request.user, ordered=False):
                    prescription.items.add(item)

                # After prescription is created, get all PrescriptionItem objects set to ordered=False and set them to ordered=True
                prescription_item_qs = PrescriptionItem.objects.filter(
                    user=request.user,
                    ordered=False,
                )
                if prescription_item_qs.exists():
                    prescription_item = prescription_item_qs[0]
                    if(prescription.items.count() > 1):
                        # If items in Prescription are more than 1, get each one and set ordered=True
                        for item in PrescriptionItem.objects.filter(user=request.user, ordered=False):
                            item.ordered = True
                            item.save()
                    else:
                        prescription_item.ordered = True
                        prescription_item.save()
                else:
                    # Warning Message if PrescriptionItem does not exist
                    messages.warning(request,"Ordered == False!")
                
                # Set complete=True in Prescription after it is created
                prescription.complete = True
                prescription.save()
                print(prescription, "just placed an order.")
                print(prescription.items.count())
                messages.info(request,  f'You have confirmed your order!')
                return redirect('accounts:dashboard') 
            
        context = {
            'u_form': u_form,
            'b_form': b_form,
            'p_form': p_form,
            'surgery_form' : surgery_form,
            'dependent_form' : dependent_form,
            'saved_surgery' : saved_surgery,
            'selected_surgeries' :selected_surgeries,
            'prescription' : prescription
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
     

global surgery
def surgery(request,slug):
    try:
        surgery=None
        surgery = get_object_or_404(HospitalList, slug=slug)
        the_surgery, created = SelectSurgery.objects.get_or_create(
            user=request.user,
            surgery=surgery,
            added=True,
        )
        surgery_qs=SelectSurgery.objects.filter(user=request.user, added=False)
        surgery.added=True
        surgery.save()
        print(surgery)
        messages.info(request, "Your surgery has been selected!")
        return redirect('accounts:dashboard')
    except ObjectDoesNotExist:
        messages.warning(self.request,"Surgery Does Not Exist!")
        return redirect("accounts:dashboard")


def new_prescription(request):
    try:
        selected_surgery = get_object_or_404(SelectSurgery, user=request.user, added=True)
        # Get all medicine_item with added = False
        medicine_item = MedicineItems.objects.filter(user=request.user, added=False)
        # Create prescription item without medicine_item
        prescription_item = PrescriptionItem.objects.create(
            user=request.user,
            selected_surgery=selected_surgery,
            ordered=False,
        )
        # Since the number of MedicineItems to be created cannot be estimated/known
        # A for loop is used, each item in MedicineItems will be added to PrescriptionItem, once a PrescriptionItem is confirmed.
        # for item in medicine_item with added=False, add item to prescription_item
        for item in medicine_item:
            prescription_item.medicine_items.add(item)

        # After prescription_item is created, get all MedicineItems objects set to added=False and set them to added=True and save it
        med_item_qs = MedicineItems.objects.filter(user=request.user)
        if med_item_qs.exists():
            med_item = med_item_qs[0]
            if (prescription_item.medicine_items.count() > 1):
                # If items in PrescriptionItems are more than 1, get each one and set added=True
                for item in medicine_item:
                    item.added = True
                    item.save()
            else:
                # If items in PrescriptionItems are not more than 1, get each one and set added=True
                item.added = True
                item.save()
        messages.success(request,"You just placed an order!")
        prescription_item.save()
    except ObjectDoesNotExist:
        messages.warning(request,"Order Not Created!")
        return redirect("accounts:dashboard")
    except UnboundLocalError:
        # If an empty order is created
        prescription_item.delete()
        messages.warning(request,"No item selected!")
        return redirect("accounts:dashboard")
    except MultipleObjectsReturned:
        messages.warning(request,"MultipleObjectsReturned!")
        return redirect("accounts:dashboard")
    except ValueError:
        # Using ForeignKey to relate MedicineItems to PrecriptionItem. This error will occur. 
        print(selected_surgery)
        print(medicine_item)
        messages.warning(request,"Cannot assign 'QuerySet [<MedicineItems: item>]': 'PrescriptionItem.medicine_item' must be a 'MedicineItems' instance.!")
        return redirect("accounts:dashboard")
    except IndexError:
        # If an empty order is created
        messages.warning(request,"Please select an Item!")
        return redirect("accounts:dashboard")
    return redirect("accounts:dashboard")


def delete_medicine(request, id):
    item = get_object_or_404(MedicineItems, id=id)
    prescription_qs = Prescription.objects.filter(
        user=request.user,
        ordered=True,
    )
    prescription_item_qs = PrescriptionItem.objects.filter(
        user=request.user,
        ordered=False
    )
    # If prescription is created, target prescription_item in it
    if prescription_qs.exists():
        prescription = prescription_qs[0]
        # Targets item in prescription_item and deletes it
        if prescription_item_qs.exists():
            prescription_item = prescription_item_qs[0]
            if (prescription_item.medicine_items.count() > 1):
                prescription_item.medicine_items.remove(item)
                prescription.items.remove(prescription_item)
                item.delete()
                print("The specific item was deleted.")
                return redirect("accounts:dashboard")
            else:
                item.delete()
                prescription_item.delete()
                prescription.delete()
                print("All items were deleted.")
                return redirect("accounts:dashboard")
        else:
            # If prescription is not created, target item in it and delete it
            item.delete()
            print("Item was deleted.")
            return redirect("accounts:dashboard")
    else:
        # If prescription does not exist yet, but prescription_item is created, target item in it and delete it
        if prescription_item_qs.exists():
            prescription_item = prescription_item_qs[0]
            if (prescription_item.medicine_items.count() > 1):
                # If medicine_items in prescription_item is more than 1, delete each item
                prescription_item.medicine_items.remove(item)
                item.delete()
                print("The specific item was deleted.")
                return redirect("accounts:dashboard")
            else:
                # delete selected items
                item.delete()
                prescription_item.delete()
                print("All items were deleted.")
                return redirect("accounts:dashboard")
        else:
            # If prescription_item is not created, target item in it and delete it
            item.delete()
            messages.info(request, "Item was deleted.")
            return redirect("accounts:dashboard")


def delete_prescription_item(request, id):
    pres_item = get_object_or_404(PrescriptionItem, id=id)
    prescription_qs = Prescription.objects.filter(
        user=request.user, 
        ordered=True
    )
    # If a Precription exists
    if prescription_qs.exists():
        prescription = prescription_qs[0]
        if (prescription.items.count() > 1):
            # If items in Precription > 1, 
            # remove each PrecriptionItem in Prescription,
            # remove each MedicineItems in PrecriptionItem
            # Delete both
            prescription.items.remove(pres_item)
            pres_item.medicine_items.remove(the_item)
            the_item.delete()
            pres_item.delete()
            print("The specific order was deleted.")
            return redirect("accounts:dashboard")
        elif (prescription.items.count() == 1):
            # remove each PrecriptionItem in Prescription,
            # remove each MedicineItems in PrecriptionItem
            # Delete both
            pres_item.medicine_items.remove(the_item)
            the_item.delete()
            pres_item.delete()
            print("The prescription item was deleted.")
            return redirect("accounts:dashboard")
        else:
            item.delete()
            pres_item.delete()
            prescription.delete()
            print("All orders were deleted.")
            return redirect("accounts:dashboard")
    else:
        # If Prescription does not exists, target only PrescriptionItems.
        if (pres_item.medicine_items.count() > 1):
            # If medicine_items in PrecriptionItem > 1, 
            # for each item in medicine_items, delete each.
            medicine_item = MedicineItems.objects.filter(user=request.user,  added=True)[0]
            for i in pres_item.medicine_items.all():
                i.delete()
            print("Items were deleted.")
        elif (pres_item.medicine_items.count() == 1):
            # for each item in medicine_items, delete each.
            for i in pres_item.medicine_items.all():
                i.delete()
            print("Item was deleted.")
        else:
            i.delete()
            print("All orders were deleted.")
            return redirect("accounts:dashboard")
        pres_item.delete()
        messages.info(request, "Order was deleted.")
        return redirect("accounts:dashboard")

def delete_prescription(request, id=id):
    pres = get_object_or_404(Prescription, id=id)
    pres_item =  PrescriptionItem.objects.filter(
        user=request.user, 
        ordered=True
    )[0]
    med_item =  MedicineItems.objects.filter(
        user=request.user, 
        added=True
    )[0]
    #  If items in Precription > 1, 
    if (pres.items.count() > 1):
        # for PrecriptionItem in Precription.items,
        # Remove each from Prescription
        # for med_item in PrecriptionItem.medicine_item
        # remove each from PrescriptionItem
        # Delete both
        for pres_item in pres.items.all():
                pres.items.remove(pres_item)
                for med_item in pres_item.medicine_items.all():
                    pres_item.medicine_items.remove(med_item)
                    med_item.delete()
                pres_item.delete()
        print("PrescriptionItems were deleted!")
    elif (pres.items.count() == 1):
        for pres_item in pres.items.all():
                pres.items.remove(pres_item)
                for med_item in pres_item.medicine_items.all():
                    pres_item.medicine_items.remove(med_item)
                    med_item.delete()
                pres_item.delete()
        print("PrescriptionItems was deleted!")
    pres.delete()
    messages.info(request, "Prescription was deleted!")
    return redirect("accounts:dashboard")