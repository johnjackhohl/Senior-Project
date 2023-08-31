from django import forms
from .models import OW_Team, Roster, Comp, Match, Game, Control_Map, Escort_Hybrid_Map, Push_Map, Player, Flashpoint_Map

class OW_Team_Form(forms.ModelForm):
    class Meta:
        model = OW_Team
        fields = ['name', 'year', 'varsity']

class Roster_Form(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['ow_team_id', 'first_name', 'last_name', 'role']