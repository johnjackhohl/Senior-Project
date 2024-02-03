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
	matches = models.Match.objects.filter(ow_team_id = pk)
	for match in matches:
		games = models.Game.objects.filter(match_id = match.id)
		for game in games:
			if game.map_type == "Control":
				control_maps = models.ControlMap.objects.filter(game_id = game.id)
	context = {
		'control_maps': control_maps,
	}
	return render(request, 'data_templates/control_stats.html', context)

def escort_hybrid_stats(request, pk, map_type):
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