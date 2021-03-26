from django import forms
from .models import stockPrice

class stockModelForm(forms.ModelForm):
    class Meta:
        model = stockPrice
        fields = "__all__"
        

  
