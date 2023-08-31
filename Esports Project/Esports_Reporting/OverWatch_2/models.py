from django.db import models

# Create your models here.
class OW_Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    varsity = models.BooleanField()

class Roster(models.Model):
    id = models.BigAutoField(primary_key=True)
    ow_team_id = models.ForeignKey(OW_Team, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

class Comp(models.Model):
    id = models.BigAutoField(primary_key=True)
    tank = models.CharField(max_length=100)
    dps_1 = models.CharField(max_length=100)
    dps_2 = models.CharField(max_length=100)
    support_1 = models.CharField(max_length=100)
    support_2 = models.CharField(max_length=100)

class Match(models.Model):
    id = models.BigAutoField(primary_key=True)
    ow_team_id = models.ForeignKey(OW_Team, on_delete=models.CASCADE)
    match_type = models.CharField(max_length=100)
    date = models.DateField()
    opponent = models.CharField(max_length=100)
    mount_score = models.IntegerField()
    opponent_score = models.IntegerField()
    mount_win = models.BooleanField()

class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    map_type = models.CharField(max_length=100)
    mount_score = models.IntegerField()
    opponent_score = models.IntegerField()
    mount_win = models.BooleanField()
    notes = models.TextField(null=True)

class Control_Map(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    map_name = models.CharField(max_length=100) 
    map_sub_name = models.CharField(max_length=100)
    round = models.IntegerField()
    mount_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="control_mount_comp")
    opponent_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="control_opponent_comp")
    mount_percent = models.IntegerField()
    opponent_percent = models.IntegerField()

class Escort_Hybrid_Map(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    map_name = models.CharField(max_length=100) 
    attack_first = models.BooleanField()
    mount_attack_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="hybrid_payload_mount_attack_comp")
    opponent_defence_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="hybrid_payload_opponent_defence_comp")
    mount_defence_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="hybrid_payload_mount_defence_comp")
    opponent_attack_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="hybrid_payload_opponent_attack_comp")

class Push_Map(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    map_name = models.CharField(max_length=100) 
    mount_distance = models.IntegerField()
    opponent_distance = models.IntegerField()
    mount_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="push_mount_comp")
    opponent_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="push_opponent_comp")

class Flashpoint_Map(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    map_name = models.CharField(max_length=100) 
    point_number = models.IntegerField()
    mount_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="flashpoit_mount_comp")
    opponent_comp = models.ForeignKey(Comp, on_delete=models.CASCADE, related_name="flashpoint_opponent_comp")

class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    roster_id = models.ForeignKey(Roster, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    hero = models.CharField(max_length=100)
    kills = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    damage = models.IntegerField(null=True)
    healing = models.IntegerField(null=True)