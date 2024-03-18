from django.db.models import Q
from django.shortcuts import render
from OverWatch_2 import models
from collections import defaultdict
from OverWatch_2.classes import map_classes

def player_data(request, pk):
	"""This function is used to display a player's data.

	Args:
		request
		pk (int): primary key of the player to display

	Returns:
		render: returns a rendred html page with a player's data
	"""
	player = models.Roster.objects.get(id=pk)
	context = {
		'player': player,
		 }
	return render(request, 'data_templates/player_data.html', context)

def control_stats(request, pk):
	"""This function is used to display a team's control map stats.

	Args:
		request
		pk (int): team's primary key

	Returns:
		render: returns a rendred html page with a team's control map stats
	"""
	control_maps = []
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Control":
				for map in models.ControlMap.objects.filter(game_id = game.id):
					control_maps.append(map)
	controlMapsStats = get_control_map_stats(control_maps)
	context = {
		'controlMapsStats': controlMapsStats,
		'team': models.OwTeam.objects.get(id=pk),
	}
	return render(request, 'data_templates/control_stats.html', context)

def get_control_map_stats(control_maps):
	maps = {}
	for map in control_maps:
		tank = map.mount_tank
		dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
		support_players = sorted([map.mount_support_1, map.mount_support_2])
		opp_tank = map.opponent_tank
		opp_dps_players = sorted([map.opponent_dps_1, map.opponent_dps_2])
		opp_support_players = sorted([map.opponent_support_1, map.opponent_support_2])
		is_win = map.mount_percent > map.opponent_percent

		if map.map_name not in maps:
			maps[map.map_name] = map_classes.Control_Map(map.map_name)

		# Ensure the SubMap exists
		maps[map.map_name].add_sub_map(map.map_sub_name)
		comp = map_classes.Composition(tank, dps_players, support_players)
		opp_comp = map_classes.Composition(opp_tank, opp_dps_players, opp_support_players)
		comp.total += 1
		opp_comp.total += 1
		if is_win:
			maps[map.map_name].sub_maps[map.map_sub_name].mount_wins += 1
			comp.wins += 1
		else:
			opp_comp.wins += 1

		# Now, add the composition to the SubMap
		maps[map.map_name].sub_maps[map.map_sub_name].add_mount_composition(comp)
		maps[map.map_name].sub_maps[map.map_sub_name].add_opponent_composition(opp_comp)

	return maps

def clash_stats(request, pk):
	"""This function is used to display a team's clash map stats

	Args:
		request 
		pk (int): team's primary key 
	"""
	clash_maps = []
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Clash":
				for map in models.ClashMap.objects.filter(game_id = game.id):
					clash_maps.append(map)
	clashMapStats = get_clash_map_stats(clash_maps)
	for map in clashMapStats:

		print(clashMapStats[map].top_mount_composition.tank)
	context = {
		'clashMapStats' : clashMapStats,
		'team': models.OwTeam.objects.get(id=pk)
	}
	return render(request, 'data_templates/clash_stats.html', context)

def get_clash_map_stats(clash_maps):
	maps = {}
	for map in clash_maps:
		tank = map.mount_tank
		dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
		support_players = sorted([map.mount_support_1, map.mount_support_2])
		opp_tank = map.opponent_tank
		opp_dps_players = sorted([map.opponent_dps_1, map.opponent_dps_2])
		opp_support_players = sorted([map.opponent_support_1, map.opponent_support_2])
		
	
		is_win = map.game_id.mount_win

		if map.map_name not in maps:
			maps[map.map_name] = map_classes.Clash_Map(map.map_name)
		else:
			maps[map.map_name].total += 1

		comp = map_classes.Composition(tank, dps_players, support_players)
		opp_comp = map_classes.Composition(opp_tank, opp_dps_players, opp_support_players)
		comp.total += 1
		opp_comp.total += 1
		if is_win:
			maps[map.map_name].mount_wins += 1
			comp.wins += 1
		else:
			opp_comp.wins += 1

		# Now, add the composition to the SubMap
		maps[map.map_name].add_mount_composition(comp)
		maps[map.map_name].add_opponent_composition(opp_comp)

	return maps