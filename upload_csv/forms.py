from .models import Csv
from django import forms

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',) 
        widget = {
            'file_name': forms.FileInput(attrs={'class': 'form-control'})
        }