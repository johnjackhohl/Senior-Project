from django.db.models import Q
from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from collections import defaultdict

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
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Control":
				control_maps = models.ControlMap.objects.filter(game_id = game.id)
	controlMapsStats = get_control_maps(pk)
	print(controlMapsStats)
	context = {
		'control_maps': control_maps,
		'controlMapsStats': controlMapsStats,
	}
	return render(request, 'data_templates/control_stats.html', context)

def get_control_maps(pk):
	controlMaps = {}
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Control":
				control_maps = models.ControlMap.objects.filter(game_id = game.id)
				for map in control_maps:
					if map.map_name not in controlMaps:
						controlMaps[map.map_name] ={}
					if map.map_sub_name not in controlMaps[map.map_name]:
						controlMaps[map.map_name][map.map_sub_name] = {"total": 0, "wins": 0, "winrate": 0, "comp": {}}
					controlMaps[map.map_name][map.map_sub_name]["total"] += 1
					if map.mount_percent > map.opponent_percent:
						controlMaps[map.map_name][map.map_sub_name]["wins"] += 1
					
					dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
					support_players = sorted([map.mount_support_1, map.mount_support_2])
					comp_key = (map.mount_tank, tuple(dps_players), tuple(support_players))

					if comp_key not in controlMaps[map.map_name][map.map_sub_name]["comp"]:
						controlMaps[map.map_name][map.map_sub_name]["comp"][comp_key] = {"total": 0, "wins": 0, "winrate": 0}
					controlMaps[map.map_name][map.map_sub_name]["comp"][comp_key]["total"] += 1
					if map.mount_percent > map.opponent_percent:
						controlMaps[map.map_name][map.map_sub_name]["comp"][comp_key]["wins"] += 1

	for map in controlMaps:
		for sub_map in controlMaps[map]:
			controlMaps[map][sub_map]["winrate"] = round(controlMaps[map][sub_map]["wins"] / controlMaps[map][sub_map]["total"] * 100, 2)
		for comp in controlMaps[map][sub_map]["comp"]:
			controlMaps[map][sub_map]["comp"][comp]["winrate"] = round(controlMaps[map][sub_map]["comp"][comp]["wins"] / controlMaps[map][sub_map]["comp"][comp]["total"] * 100, 2)
	return controlMaps

						


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