from django import forms
from .models import OW_Team, Roster

class OW_Team_Form(forms.ModelForm):
    class Meta:
        model = OW_Team
        fields = ['name', 'year_fall', 'year_spring', 'varsity']

class Roster_Form(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['ow_team_id','first_name', 'last_name', 'role']
