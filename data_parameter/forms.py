from django import forms 
from .models import getempdetails

class empdetails(forms.ModelForm):
    empname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    job = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = getempdetails
        fields = ['empname', 'job', 'email', 'username', 'password']
        

