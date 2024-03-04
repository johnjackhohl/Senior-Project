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
	controlMapsStats = get_control_map(control_maps, True)
	oppComp = get_control_map(control_maps, False)
	for map_name, map_obj in oppComp.items():
		print(f"Map: {map_name}")
		for sub_map_name, sub_map_obj in map_obj.sub_maps.items():
			top_comp = sub_map_obj.top_composition()
			if top_comp:
				print(f"  Sub Map: {sub_map_name}, Sub_map Total: {sub_map_obj.total}, Top Comp: Tank: {top_comp.tank}, DPS: {top_comp.dps}, Support: {top_comp.support}, Total: {top_comp.total} Winrate: {top_comp.winrate}")

	context = {
		'controlMapsStats': controlMapsStats,
		'team': models.OwTeam.objects.get(id=pk),
		'oppComp': oppComp,
	}
	return render(request, 'data_templates/control_stats.html', context)


def get_control_map(control_maps, mount):
	opponent_maps = {}
	for map in control_maps:
		tank = map.opponent_tank
		dps_players = sorted([map.opponent_dps_1, map.opponent_dps_2])
		support_players = sorted([map.opponent_support_1, map.opponent_support_2])
		if mount:
			is_win = map.mount_percent > map.opponent_percent
		else:
			is_win = map.opponent_percent > map.mount_percent

		if map.map_name not in opponent_maps:
			opponent_maps[map.map_name] = map_classes.Control_Flashpoint_Map(map.map_name)

		# Ensure the SubMap exists
		opponent_maps[map.map_name].add_sub_map(map.map_sub_name)

		comp = map_classes.Composition(tank, dps_players, support_players)
		comp.total += 1
		if is_win:
			comp.wins += 1

		# Now, add the composition to the SubMap
		opponent_maps[map.map_name].sub_maps[map.map_sub_name].add_composition(comp)

	return opponent_maps




def escort_hybrid_stats(request, pk, map_type):
	"""This function is used to display a team's escort/hybrid map stats.

	Args:
		request
		pk (int): primary key of the team to display
		map_type (string): either "Escort" or "Hybrid"

	Returns:
		render: returns a rendred html page with a team's escort/hybrid map stats
	"""
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id, map_type = map_type)
		for game in games:
			if game.map_type == map_type:
				escort_hybrid_maps = models.EscortHybridMap.objects.filter(game_id = game.id)
	context = {
		'escort_hybrid_maps': escort_hybrid_maps,
		'map_type': map_type,
	}
	return render(request, 'data_templates/escort_hybrid_stats.html', context)

def clash_stats(request, pk):
	"""This function is used to display a team's clash map stats.

	Args:
		request 
		pk (int): team's primary key

	Returns:
		render: returns a rendred html page with a team's clash map stats
	"""
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id, map_type = "Clash")
		for game in games:
			if game.map_type == "Clash":
				clash_maps = models.ClashMap.objects.filter(game_id = game.id)
	context = {
		'clash_maps': clash_maps,
	}
	return render(request, 'data_templates/clash_stats.html', context)

def flashpoint_stats(request, pk):
	"""This function is used to display a team's flashpoint map stats.

	Args:
		request
		pk (int): team's primary key

	Returns:
		render: returns a rendred html page with a team's flashpoint map stats
	"""
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id, map_type = "Flashpoint")
		for game in games:
			if game.map_type == "Flashpoint":
				flashpoint_maps = models.FlashpointMap.objects.filter(game_id = game.id)
	context = {
		'flashpoint_maps': flashpoint_maps,
	}
	return render(request, 'data_templates/flashpoint_stats.html', context)

def push_stats(request, pk):
	"""This function is used to display a team's push map stats.

	Args:
		request
		pk (int): team's primary key

	Returns:
		render: returns a rendred html page with a team's push map stats
	"""
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id, map_type = "Push")
		for game in games:
			if game.map_type == "Push":
				push_maps = models.PushMap.objects.filter(game_id = game.id)
	context = {
		'push_maps': push_maps,
	}
	return render(request, 'data_templates/push_stats.html', context)