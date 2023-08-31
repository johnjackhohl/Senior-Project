from django import forms
from .models import OW_Team

class OW_Team_Form(forms.ModelForm):
    class Meta:
        model = OW_Team
        fields = ['name', 'year_fall', 'year_spring', 'varsity']