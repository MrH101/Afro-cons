from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orer
        fields = ['product_name','quantity','price']
        widgets = {
            'product_name':forms.TextInput(attrs = {'placeholder':"enter product name"}),
            'quantity':forms.NumberInput(attrs = {'placeholder':"enter quantity"}),
            'price':forms.NumberInput(attrs = {'placeholder':"enter price per unity"}),

        }


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status' :
            forms.Select(attrs={'class':'form_select'})
        }