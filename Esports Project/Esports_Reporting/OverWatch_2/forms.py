from django import forms
from .models import *

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
		fields = ['game_id', 'map_name', 'map_sub_name', 'round', 'mount_tank', 'mount_dps_1', 'mount_dps_2', 'mount_support_1', 
				  'mount_support_2', 'opponent_tank', 'opponent_dps_1', 'opponent_dps_2', 'opponent_support_1', 'opponent_support_2', 'mount_percent', 'opponent_percent']

class Escort_Hybrid_Map_Form(forms.ModelForm):
	class Meta:
		model = Escort_Hybrid_Map
		fields = ['game_id', 'is_Escort', 'map_name', 'attack_first', 'mount_attack_tank', 'mount_attack_dps_1', 
				  'mount_attack_dps_2', 'mount_attack_support_1', 'mount_attack_support_2', 'mount_defense_tank', 
				  'mount_defense_dps_1', 'mount_defense_dps_2', 'mount_defense_support_1', 
				  'mount_defense_support_2', 'opponent_attack_tank', 'opponent_attack_dps_1', 
				  'opponent_attack_dps_2', 'opponent_attack_support_1', 'opponent_attack_support_2', 
				  'opponent_defense_tank', 'opponent_defense_dps_1', 'opponent_defense_dps_2', 'opponent_defense_support_1', 
				  'opponent_defense_support_2']

class Push_Map_Form(forms.ModelForm):
	class Meta:
		model = Push_Map
		fields = ['game_id', 'map_name', 'mount_distance', 'opponent_distance', 'mount_tank', 'mount_dps_1',
					'mount_dps_2', 'mount_support_1', 'mount_support_2', 'opponent_tank', 'opponent_dps_1',
					'opponent_dps_2', 'opponent_support_1', 'opponent_support_2']

class Flashpoint_Map_Form(forms.ModelForm):
	class Meta:
		model = Flashpoint_Map
		fields = ['game_id', 'map_name', 'point_number', 'mount_percent','opponent_percent', 'mount_tank', 'mount_dps_1', 'mount_dps_2', 
				  'mount_support_1', 'mount_support_2', 'opponent_tank', 'opponent_dps_1',
					'opponent_dps_2', 'opponent_support_1', 'opponent_support_2']

class Player_Form(forms.ModelForm):
	class Meta:
		model = Player
		fields = ['roster_id', 'control_id', 'push_id', 'flashpoint_id', 'escort_hybrid_id', 'hero', 'role', 'is_defense', 'kills', 'deaths', 'assists', 'damage', 'healing']

class Add_Hero_Form(forms.ModelForm):
	class Meta:
		model = Hero
		fields = ['hero_name', 'role', 'hero_image']

class Add_Map_Form(forms.ModelForm):
	class Meta:
		model = Map
		fields = ['map_name', 'map_type', 'map_image']

class Add_Sub_Map(forms.ModelForm):
    class Meta:
        model = Sub_Map
        fields = ['map_id', 'sub_map_name', 'sub_map_image']
        widgets = {
            'map_id': forms.HiddenInput(),
        }

class Add_Match_Type_Form(forms.ModelForm):
	class Meta:
		model = Match_Type
		fields = ['match_type']

class Delete_Map_Form(forms.Form):
	map_type = forms.CharField(max_length=100)
	map_name = forms.CharField(max_length=100)

class Delete_Hero_Form(forms.Form):
	hero_name = forms.CharField(max_length=100)

class Delete_Match_Type_Form(forms.Form):
	match_type = forms.CharField(max_length=100)

class Delete_Roster_Player_Form(forms.Form):
	player_id = forms.IntegerField()