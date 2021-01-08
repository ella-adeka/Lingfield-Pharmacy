from django import forms
from .models import *
from accounts.forms import *
from accounts.models import *
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth import (
    authenticate,
    get_user_model

)
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('Credit', 'Credit'),
    ('Debit', 'Debit'),
    ('Paypal', 'Paypal')
)


class CheckOutDelivery(forms.ModelForm):
    payment = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

    class Meta():
        model = Order
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    name_on_card = forms.CharField()
    credit_card_number = forms.CharField()
    expiration = forms.CharField()
    cvv = forms.CharField()

    class Meta():
        model = Payment
        fields = {'name_on_card','credit_card_number','expiration','cvv'};    

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args,**kwargs)
        self.fields['cvv'].label = "CVV"