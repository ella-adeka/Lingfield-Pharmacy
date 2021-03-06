from django import forms
from .models import *
from medicines.models import Medicine
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth import (
    authenticate,
    get_user_model

)
from django_countries.fields import CountryField


# Create your form choices here.
GENDER_CHOICES = (
    ('Female','Female'),
    ('Male','Male'),
    ('Not Set','Not Set'),
    ('Other','Other'),
)

REMINDER_CHOICES = (
    ('Never','Never'),
    ('Once','Once'),
    ('Regularly','Regularly'),
)

RECEIVAL_CHOICES = (
    ('Courier','Courier'),
)


# Create your forms here.
class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(),help_text='')
    password2 =  forms.CharField(widget=forms.PasswordInput(),help_text='')
    
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password1', 'password2')
        help_texts = {
            'username': None,
            'email': None,            
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "Surname"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

class UserBirthDateForm(forms.ModelForm):
   
    class Meta():
        model = UserBirthDate
        fields = ('birth_date',)
        widgets = {
            'birth_date': forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
        }    

class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Gender',required=True, choices=GENDER_CHOICES, initial='N')

    classed_as_vulnerable = forms.BooleanField(required=False)
    housebound = forms.BooleanField(required=False)
    like_to_receive_email = forms.BooleanField(required=False)
    
    class Meta():
        model = UserProfile
        fields = ('classed_as_vulnerable','housebound','like_to_receive_email','country','uk_postcode_lookup','house_number','gender','street','town','county','postcode','nhs_no','telephone_no','mobile_no')
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['classed_as_vulnerable'].label = "I am classed as vulnerable by my surgery"
        self.fields['housebound'].label = "I am housebound"
        self.fields['like_to_receive_email'].label = "I would like to receive information via email"
       
        

# ---------------------------------------------------------------   UPDATE FORMS    ----------------------------------------------------------------------------------#
class UpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = {'username','email','first_name','last_name',}
        help_texts = {
            'username': None,
            'email': None,  
            'birth_date': 'yyyy-mm-dd',          
        }

class UpdateBirthDateForm(forms.ModelForm):
   
    class Meta():
        model = UserBirthDate
        fields = {'birth_date',}

class UpdateProfileForm(forms.ModelForm):
   
    class Meta():
        model = UserProfile
        fields = {'country','uk_postcode_lookup','house_number','street','town','county','postcode','country','uk_postcode_lookup','house_number','street','town','county','postcode'}
        
# ---------------------------------------------------------------  END OF UPDATE FORMS    ----------------------------------------------------------------------------------#


# ---------------------------------------------------------------   SURGERY FORM    ----------------------------------------------------------------------------------#
class AddSurgeryForm(forms.ModelForm):
   
    class Meta():
        model = AddSurgery
        fields = {'surgery_name','country','uk_postcode_lookup','house_number','address'}

# ---------------------------------------------------------------   END OF SURGERY FORM    ----------------------------------------------------------------------------------#


# ---------------------------------------------------------------   DEPENDENT FORM    ----------------------------------------------------------------------------------#
class DependentForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Gender',required=True, choices=GENDER_CHOICES, initial='None')

    vulnerable_patient = forms.BooleanField(required=False)
    housebound_patient = forms.BooleanField(required=False)

    class Meta():
        model = Dependent
        fields = {'relation','first_name','middle_names','last_name','birth_date','gender','vulnerable_patient','housebound_patient','landline_telephone_no','mobile_no','country','street','town','county','postcode','notes','nhs_no'}
        widgets = {
            'birth_date': forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
        } 

    def __init__(self, *args, **kwargs):
        super(DependentForm, self).__init__(*args, **kwargs)
        self.fields['vulnerable_patient'].label = "Patient is Vulnerable"
        self.fields['housebound_patient'].label = "Patient is Housebound"
       
# ---------------------------------------------------------------   END OF DEPENDENT FORM    ----------------------------------------------------------------------------------#



# ---------------------------------------------------------------   MEDICINE FORM    ----------------------------------------------------------------------------------#


class MedicineItemsForm(forms.ModelForm):
    reminder = forms.ChoiceField(label='Remind me to order this item',required=True, choices=REMINDER_CHOICES, initial='N')
    class Meta():
        model = MedicineItems
        fields = {'item','quantity'}
               
# ---------------------------------------------------------------   END OF MEDICINE FORM    ----------------------------------------------------------------------------------#

# ---------------------------------------------------------------   ORDER FORM    ----------------------------------------------------------------------------------#

class OrderForm(forms.ModelForm):
    receival = forms.ChoiceField(label='Remind me to order this item',required=True, choices=RECEIVAL_CHOICES, initial='N')
    class Meta():
        model = Prescription
        fields = {'receival','prescription_note','delivery_note'}

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['receival'].label = "How do you want to receive your prescription?"
        self.fields['prescription_note'].label = "Add a note to your prescription order..."
        self.fields['prescription_note'].required = False
        self.fields['delivery_note'].label = "Add a delivery note..."
        self.fields['delivery_note'].required = False

    
        
# ---------------------------------------------------------------   END OF ORDER FORM    ----------------------------------------------------------------------------------#

