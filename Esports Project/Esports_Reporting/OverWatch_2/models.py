from django.db import models

# Create your models here.
class OwTeam(models.Model):
	"""This model is used to store Overwatch teams."""
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=100)
	year_fall = models.IntegerField()
	year_spring = models.IntegerField()
	varsity = models.BooleanField()

class Roster(models.Model):
	"""This Model is used to store Overwatch players for the teams."""
	id = models.BigAutoField(primary_key=True)
	ow_team_id = models.ForeignKey(OwTeam, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	role = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)

class Match(models.Model):
	"""This model is used to store Overwatch matches."""
	id = models.BigAutoField(primary_key=True)
	ow_team_id = models.ForeignKey(OwTeam, on_delete=models.CASCADE)
	match_type = models.CharField(max_length=100)
	opponent = models.CharField(max_length=100)
	mount_score = models.IntegerField()
	opponent_score = models.IntegerField()
	mount_win = models.BooleanField()
	match_date = models.DateField()

class Game(models.Model):
	"""This model is used to store Overwatch games."""
	id = models.BigAutoField(primary_key=True)
	match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
	map_type = models.CharField(max_length=100)
	mount_score = models.IntegerField()
	opponent_score = models.IntegerField()
	mount_win = models.BooleanField()
	notes = models.TextField(null=True, blank=True)

	def get_maps(self):
		"""This function is used to get the maps for the game.

		Returns:
			self: addes the maps to the game object
		"""
		if self.map_type == "Control":
			return self.control_map_set.all()
		elif self.map_type in ["Escort", "Hybrid"]:
			return self.escort_hybrid_map_set.all()
		elif self.map_type == "Push":
			return self.push_map_set.all()
		elif self.map_type == "Clash":
			return self.clash_map_set.all()
		else:
			return self.flashpoint_map_set.all()

class ControlMap(models.Model):
	"""This model is used to store Overwatch control maps."""
	id = models.BigAutoField(primary_key=True)
	game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="control_map_set")
	map_name = models.CharField(max_length=100) 
	map_sub_name = models.CharField(max_length=100)
	round = models.IntegerField()
	mount_tank = models.CharField(max_length=100)
	mount_dps_1 = models.CharField(max_length=100)
	mount_dps_2 = models.CharField(max_length=100)
	mount_support_1 = models.CharField(max_length=100)
	mount_support_2 = models.CharField(max_length=100)
	opponent_tank = models.CharField(max_length=100)
	opponent_dps_1 = models.CharField(max_length=100)
	opponent_dps_2 = models.CharField(max_length=100)
	opponent_support_1 = models.CharField(max_length=100)
	opponent_support_2 = models.CharField(max_length=100)
	mount_percent = models.IntegerField()
	opponent_percent = models.IntegerField()

class EscortHybridMap(models.Model):
	"""This model is used to store Overwatch escort and hybrid maps."""
	id = models.BigAutoField(primary_key=True)
	game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="escort_hybrid_map_set")
	is_Escort = models.BooleanField()
	map_name = models.CharField(max_length=100) 
	attack_first = models.BooleanField()
	mount_attack_tank = models.CharField(max_length=100)
	mount_attack_dps_1 = models.CharField(max_length=100)
	mount_attack_dps_2 = models.CharField(max_length=100)
	mount_attack_support_1 = models.CharField(max_length=100)
	mount_attack_support_2 = models.CharField(max_length=100)
	opponent_defense_tank = models.CharField(max_length=100)
	opponent_defense_dps_1 = models.CharField(max_length=100)
	opponent_defense_dps_2 = models.CharField(max_length=100)
	opponent_defense_support_1 = models.CharField(max_length=100)
	opponent_defense_support_2 = models.CharField(max_length=100)
	mount_defense_tank = models.CharField(max_length=100)
	mount_defense_dps_1 = models.CharField(max_length=100)
	mount_defense_dps_2 = models.CharField(max_length=100)
	mount_defense_support_1 = models.CharField(max_length=100)
	mount_defense_support_2 = models.CharField(max_length=100)
	opponent_attack_tank = models.CharField(max_length=100)
	opponent_attack_dps_1 = models.CharField(max_length=100)
	opponent_attack_dps_2 = models.CharField(max_length=100)
	opponent_attack_support_1 = models.CharField(max_length=100)
	opponent_attack_support_2 = models.CharField(max_length=100)

class PushMap(models.Model):
	"""This model is used to store Overwatch push maps."""
	id = models.BigAutoField(primary_key=True)
	game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="push_map_set")
	map_name = models.CharField(max_length=100) 
	mount_distance = models.IntegerField()
	opponent_distance = models.IntegerField()
	mount_tank = models.CharField(max_length=100)
	mount_dps_1 = models.CharField(max_length=100)
	mount_dps_2 = models.CharField(max_length=100)
	mount_support_1 = models.CharField(max_length=100)
	mount_support_2 = models.CharField(max_length=100)
	opponent_tank = models.CharField(max_length=100)
	opponent_dps_1 = models.CharField(max_length=100)
	opponent_dps_2 = models.CharField(max_length=100)
	opponent_support_1 = models.CharField(max_length=100)
	opponent_support_2 = models.CharField(max_length=100)

class FlashpointMap(models.Model):
	"""This model is used to store Overwatch flashpoint maps."""
	id = models.BigAutoField(primary_key=True)
	game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="flashpoint_map_set")
	map_name = models.CharField(max_length=100) 
	point_number = models.IntegerField()
	mount_percent = models.IntegerField()
	opponent_percent = models.IntegerField()
	mount_tank = models.CharField(max_length=100)
	mount_dps_1 = models.CharField(max_length=100)
	mount_dps_2 = models.CharField(max_length=100)
	mount_support_1 = models.CharField(max_length=100)
	mount_support_2 = models.CharField(max_length=100)
	opponent_tank = models.CharField(max_length=100)
	opponent_dps_1 = models.CharField(max_length=100)
	opponent_dps_2 = models.CharField(max_length=100)
	opponent_support_1 = models.CharField(max_length=100)
	opponent_support_2 = models.CharField(max_length=100)

class ClashMap(models.Model):
	"""This model is used to store Overwatch clash maps."""
	id = models.BigAutoField(primary_key=True)
	game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="clash_map_set")
	map_name = models.CharField(max_length=100) 
	mount_tank = models.CharField(max_length=100)
	mount_dps_1 = models.CharField(max_length=100)
	mount_dps_2 = models.CharField(max_length=100)
	mount_support_1 = models.CharField(max_length=100)
	mount_support_2 = models.CharField(max_length=100)
	opponent_tank = models.CharField(max_length=100)
	opponent_dps_1 = models.CharField(max_length=100)
	opponent_dps_2 = models.CharField(max_length=100)
	opponent_support_1 = models.CharField(max_length=100)
	opponent_support_2 = models.CharField(max_length=100)
	A_point_win = models.BooleanField()
	B_point_win = models.BooleanField()
	C_point_win = models.BooleanField()
	D_point_win = models.BooleanField()
	E_point_win = models.BooleanField()

class Player(models.Model):
	"""This model is used to store Overwatch players for the maps"""
	id = models.BigAutoField(primary_key=True)
	roster_id = models.ForeignKey(Roster, on_delete=models.CASCADE)
	control_id = models.ForeignKey(ControlMap, on_delete=models.CASCADE, null=True, blank=True, related_name="control_players")
	push_id = models.ForeignKey(PushMap, on_delete=models.CASCADE, null=True, blank=True, related_name="push_players")
	flashpoint_id = models.ForeignKey(FlashpointMap, on_delete=models.CASCADE, null=True, blank=True, related_name="flashpoint_players")
	escort_hybrid_id = models.ForeignKey(EscortHybridMap, on_delete=models.CASCADE, null=True, blank=True, related_name="escort_hybrid_players")
	clash_id = models.ForeignKey(ClashMap, on_delete=models.CASCADE, null=True, blank=True, related_name="clash_players")
	role = models.CharField(max_length=100)
	hero = models.CharField(max_length=100)
	is_defense = models.BooleanField(default=False)
	kills = models.IntegerField(null=True, blank=True)
	deaths = models.IntegerField(null=True, blank=True)
	assists = models.IntegerField(null=True, blank=True)
	damage = models.IntegerField(null=True, blank=True)
	healing = models.IntegerField(null=True, blank=True)
 
class Map(models.Model):
	"""This model is used to store Overwatch maps."""
	id = models.BigAutoField(primary_key=True)
	map_name = models.CharField(max_length=100)
	map_type = models.CharField(max_length=100)
	map_image = models.ImageField(upload_to='images/')

class SubMap(models.Model):
	"""This model is used to store Overwatch sub maps."""
	id = models.BigAutoField(primary_key=True)
	map_id = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='sub_map_set')
	sub_map_name = models.CharField(max_length=100)

class Hero(models.Model):
	"""This model is used to store Overwatch heroes."""
	id = models.BigAutoField(primary_key=True)
	hero_name = models.CharField(max_length=100)
	role = models.CharField(max_length=100)
	hero_image = models.ImageField(upload_to='images/')

class MatchType(models.Model):
	"""This model is used to store Overwatch match types."""
	id = models.BigAutoField(primary_key=True)
	match_type = models.CharField(max_length=100)