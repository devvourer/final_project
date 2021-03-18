from django import forms
from .models import Order


class OrderCreateForm(forms.Form):
    address = forms.CharField()
    postal_code = forms.CharField(max_length=20)
    city = forms.CharField()
