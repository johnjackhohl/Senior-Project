from django import forms
from .models import OW_Team, Roster, Match, Game, Control_Map, Escort_Hybrid_Map, Flashpoint_Map, Push_Map

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

class Escort_Hybrid_Map_Form(forms.ModelForm):
    class Meta:
        model = Escort_Hybrid_Map
        fields = ['game_id', 'is_Escort', 'map_name', 'attack_first', 'mount_attack_tank', 'mount_attack_dps_1', 'mount_attack_dps_2', 'mount_attack_support_1', 'mount_attack_support_2', 'mount_attack_time', 'mount_defense_tank', 'mount_defense_dps_1', 'mount_defense_dps_2', 'mount_defense_support_1', 'mount_defense_support_2', 'mount_defense_time', 'opponent_attack_tank', 'opponent_attack_dps_1', 'opponent_attack_dps_2', 'opponent_attack_support_1', 'opponent_attack_support_2', 'opponent_attack_time', 'opponent_defense_tank', 'opponent_defense_dps_1', 'opponent_defense_dps_2', 'opponent_defense_support_1', 'opponent_defense_support_2', 'opponent_defense_time', 'mount_distance', 'opponent_distance']

class Flashpoint_Map_Form(forms.ModelForm):
    class Meta:
        model = Flashpoint_Map
        field = ['game_id', 'map_name', 'point_number', 'mount_tank', 'mount_dps_1', 'mount_dps_2', 'mount_support_1', 'mount_support_2', 'opponent_tank', 'opponent_dps_1', 'opponent_dps_2', 'opponent_support_1', 'opponent_support_2']

class Push_Map_Form(forms.ModelForm):
    class Meta:
        model=Push_Map
        field = ['game_id', 'map_name', 'mount_distance', 'opponent_distance', 'mount_tank', 'mount_dps_1', 'mount_dps_2', 'mount_support_1', 'mount_support_2', 'opponent_tank', 'opponent_dps_1', 'opponent_dps_2', 'opponent_support_1', 'opponent_support_2']