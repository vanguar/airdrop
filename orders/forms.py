from django import forms
from .models import *


class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True) # required=True - означает, что это поле нам нужно
    phone = forms.CharField(required=True)