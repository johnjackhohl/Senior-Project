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

def flashpoint_stats(request, pk):
	"""This function is used to display a team's flashpoint map stats

	Args:
		request 
		pk (int): team's primary key 
	"""
	flashpoint_maps = []
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Flashpoint":
				for map in models.FlashpointMap.objects.filter(game_id = game.id):
					flashpoint_maps.append(map)
	flashpointMapStats = get_flashpoint_map_stats(flashpoint_maps)
	context = {
		'flashpointMapStats' : flashpointMapStats,
		'team': models.OwTeam.objects.get(id=pk)
	}
	return render(request, 'data_templates/flashpoint_stats.html', context)

def get_flashpoint_map_stats(flashpoint_maps):
	maps = {}
	for map in flashpoint_maps:
		tank = map.mount_tank
		dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
		support_players = sorted([map.mount_support_1, map.mount_support_2])
		opp_tank = map.opponent_tank
		opp_dps_players = sorted([map.opponent_dps_1, map.opponent_dps_2])
		opp_support_players = sorted([map.opponent_support_1, map.opponent_support_2])
		is_win = map.mount_percent > map.opponent_percent

		if map.map_name not in maps:
			maps[map.map_name] = map_classes.Flashpoint_Map(map.map_name)

		maps[map.map_name].add_point(map.point_number)
		comp = map_classes.Composition(tank, dps_players, support_players)
		opp_comp = map_classes.Composition(opp_tank, opp_dps_players, opp_support_players)
		comp.total += 1
		opp_comp.total += 1
		if is_win:
			maps[map.map_name].points[map.point_number].mount_wins += 1
			comp.wins += 1
		else:
			opp_comp.wins += 1

		# Now, add the composition to the SubMap
		maps[map.map_name].points[map.point_number].add_mount_composition(comp)
		maps[map.map_name].points[map.point_number].add_opponent_composition(opp_comp)

	return maps

def push_stats(request, pk):
	"""This function is used to display a team's push map stats

	Args:
		request 
		pk (int): team's primary key 
	"""
	push_maps = []
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Push":
				for map in models.PushMap.objects.filter(game_id = game.id):
					push_maps.append(map)
	pushMapStats = get_push_map_stats(push_maps)
	context = {
		'pushMapStats' : pushMapStats,
		'team': models.OwTeam.objects.get(id=pk)
	}
	return render(request, 'data_templates/push_stats.html', context)

def get_push_map_stats(push_maps):
	maps = {}
	for map in push_maps:
		tank = map.mount_tank
		dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
		support_players = sorted([map.mount_support_1, map.mount_support_2])
		opp_tank = map.opponent_tank
		opp_dps_players = sorted([map.opponent_dps_1, map.opponent_dps_2])
		opp_support_players = sorted([map.opponent_support_1, map.opponent_support_2])
		is_win = map.mount_distance > map.opponent_distance

		if map.map_name not in maps:
			maps[map.map_name] = map_classes.Push_Map(map.map_name)
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

		maps[map.map_name].add_mount_distance(map.mount_distance)
		maps[map.map_name].add_opponent_distance(map.opponent_distance)
		maps[map.map_name].add_mount_composition(comp)
		maps[map.map_name].add_opponent_composition(opp_comp)
	return maps

def escort_hybrid_stats(request, pk, map_type):
	"""This function is used to display a team's escort and hybrid map stats

	Args:
		request 
		pk (int): team's primary key 
	"""
	escort_hybrid_maps = []
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if map_type == "Escort":
				if game.map_type == "Escort":
					for map in models.EscortHybridMap.objects.filter(game_id = game.id):
						escort_hybrid_maps.append(map)
			else:
				if game.map_type == "Hybrid":
					for map in models.EscortHybridMap.objects.filter(game_id = game.id):
						escort_hybrid_maps.append(map)
	escortHybridMapStats = get_escort_hybrid_map_stats(escort_hybrid_maps)
	context = {
		'map_type': map_type,
		'escortHybridMapStats' : escortHybridMapStats,
		'team': models.OwTeam.objects.get(id=pk)
	}
	return render(request, 'data_templates/escort_hybrid_stats.html', context)

def get_escort_hybrid_map_stats(escort_hybrid_maps):
	maps = {}
	for map in escort_hybrid_maps:
		mount_attack_tank = map.mount_attack_tank
		mount_attack_dps = sorted([map.mount_attack_dps_1, map.mount_attack_dps_2])
		mount_attack_support = sorted([map.mount_attack_support_1, map.mount_attack_support_2])

		mount_defense_tank = map.mount_defense_tank
		mount_defense_dps = sorted([map.mount_defense_dps_1, map.mount_defense_dps_2])
		mount_defense_support = sorted([map.mount_defense_support_1, map.mount_defense_support_2])

		opp_attack_tank = map.opponent_attack_tank
		opp_attack_dps = sorted([map.opponent_attack_dps_1, map.opponent_attack_dps_2])
		opp_attack_support = sorted([map.opponent_attack_support_1, map.opponent_attack_support_2])

		opp_defense_tank = map.opponent_defense_tank
		opp_defense_dps = sorted([map.opponent_defense_dps_1, map.opponent_defense_dps_2])
		opp_defense_support = sorted([map.opponent_defense_support_1, map.opponent_defense_support_2])

		game = models.Game.objects.get(id = map.game_id.id)
		is_win = game.mount_score > game.opponent_score

		if map.map_name not in maps:
			maps[map.map_name] = map_classes.Escort_Hybrid_Map(map.map_name)
		else:
			maps[map.map_name].total += 1
		
		mount_attack_comp = map_classes.Composition(mount_attack_tank, mount_attack_dps, mount_attack_support)
		mount_defense_comp = map_classes.Composition(mount_defense_tank, mount_defense_dps, mount_defense_support)
		opp_attack_comp = map_classes.Composition(opp_attack_tank, opp_attack_dps, opp_attack_support)
		opp_defense_comp = map_classes.Composition(opp_defense_tank, opp_defense_dps, opp_defense_support)
		
		mount_attack_comp.total += 1
		mount_defense_comp.total += 1
		opp_attack_comp.total += 1
		opp_defense_comp.total += 1

		if is_win:
			maps[map.map_name].mount_wins += 1
			mount_attack_comp.wins += 1
			mount_defense_comp.wins += 1
		else:
			opp_attack_comp.wins += 1
			opp_defense_comp.wins += 1

		maps[map.map_name].add_mount_composition(mount_attack_comp, True)
		maps[map.map_name].add_mount_composition(mount_defense_comp, False)
		maps[map.map_name].add_opponent_composition(opp_attack_comp, True)
		maps[map.map_name].add_opponent_composition(opp_defense_comp, False)

	return maps