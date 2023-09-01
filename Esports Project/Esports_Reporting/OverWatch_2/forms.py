from django import forms
from .models import OW_Team, Roster, Match, Game, Control_Map

class OW_Team_Form(forms.ModelForm):
    class Meta:
        model = OW_Team
        fields = ['name', 'year_fall', 'year_spring', 'varsity']

class Roster_Form(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['ow_team_id','first_name', 'last_name', 'role']

class Match_Form(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['ow_team_id', 'match_type','opponent', 'mount_score', 'opponent_score', 'mount_win']

class Game_Form(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['match_id', 'map_type', 'mount_score', 'opponent_score', 'mount_win', 'notes']

class Control_Map_Form(forms.ModelForm):
    class Meta:
        model = Control_Map
        fields = ['game_id', 'map_name', 'map_sub_name', 'round', 'mount_tank', 'mount_dps_1', 'mount_dps_2', 'mount_support_1', 'mount_support_2', 'opponent_tank', 'opponent_dps_1', 'opponent_dps_2', 'opponent_support_1', 'opponent_support_2', 'mount_percent', 'opponent_percent']