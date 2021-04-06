from django import forms

class buyerForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    mobile = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))