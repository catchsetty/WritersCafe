from django import forms

class OrdersForm(forms.Form):
    datefrom = forms.CharField(label='Your Name', max_length=50)