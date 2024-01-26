from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models

def ow_rosters(request):
	"""This function is used to display all Overwatch teams that have been created.

	Args:
		request

	Returns:
		render: returns a rendred html page with all Overwatch teams that have been created
	"""
	OW_Teams = forms.OwTeam.objects.all()
	return render(request, 'team_templates/OW_Rosters.html', {"OW_Teams": OW_Teams})

def ow_team_roster(request, pk):
	team, owMatches = match_history(pk)
	# get only players who is_active is True
	players = models.Roster.objects.filter(ow_team_id=team.id, is_active=True)
	heroPictures = models.Hero.objects.all()
	mapPictures = models.Map.objects.all()
	map_stats = map_winrates(pk)
	view = {
		"OW_Team": team,
		"Roster": players,
		"Hero_Pictures": heroPictures,
		"Matches": owMatches,
		"Map_Pictures": mapPictures,
		"Map_Stats": map_stats,
	}
	return render(request, 'team_templates/OW_Team_Roster.html', view)

def match_history(pk):
	"""This function is used to get all matches that a team has played.

	Args:
		pk (int): primary key of the team to get matches for

	Returns:
		model: team model of the team that matches were requested for
		model: match model of all matches that the team has played
	"""
	team = models.OwTeam.objects.get(id=pk)
	owMatches = models.Match.objects.filter(ow_team_id=pk).prefetch_related('game_set').order_by('-id')

	for match in owMatches:
		for game in match.game_set.all():
			game_maps_with_players = []  # List to hold maps and their players
			print(game.map_type)
			maps = game.get_maps()
			for map in maps:
				if game.map_type == "Control":
					players = map.control_players.all()
				elif game.map_type in ["Escort", "Hybrid"]:
					players = map.escort_hybrid_players.all()
				elif game.map_type == "Push":
					players = map.push_players.all()
				elif game.map_type == "Clash":
					players = map.clash_players.all()
				elif game.map_type == "Flashpoint":
					players = map.flashpoint_players.all()
				
				game_maps_with_players.append({
					'map': map,
					'players': players
				})

			# Attach this list to the game object
			game.maps_with_players = game_maps_with_players

	return team, owMatches

def activate_player(request, pk):
	"""This function is used to activate a player that has been deactivated, to add to the roster again

	Args:
		request
		pk (int): primary key of the player who is to be activated

	Returns:
		render: returns a rendered html page with a form to activate a player
	"""
	team = models.OwTeam.objects.get(id=pk)
	roster = models.Roster.objects.filter(ow_team_id=pk, is_active=False)
	if request.method == "POST":
		form = forms.Activate_Player_Form(request.POST)
		if form.is_valid():
			player = models.Roster.objects.get(id=form.cleaned_data["player_id"])
			player.is_active = True
			player.save()
			team = models.OwTeam.objects.get(id=player.ow_team_id.id)
			return redirect('team-roster', pk=team.id)
	else:
		form = forms.Activate_Player_Form()
	context = {
		'form': form,
		'roster': roster,
		'team_id': team.id
	}
	return render(request, 'team_templates/activate_player.html', context)

from collections import defaultdict

def map_winrates(pk):
	"""
	This function is used to get the winrates for each map type for a team.

	Args:
		pk (int): primary key of the team to get winrates for
	"""
	# Fetch all relevant games
	games = models.Game.objects.filter(match_id__ow_team_id=pk).values('map_type', 'mount_win')

	# Initialize a dictionary to store game counts and wins
	map_stats = defaultdict(lambda: {'wins': 0, 'total': 0})

	# count total and wins
	for game in games:
		map_type = game['map_type']
		map_stats[map_type]['total'] += 1
		if game['mount_win']:
			map_stats[map_type]['wins'] += 1

	# Convert defaultdict to regular dict
	map_stats = {k: dict(v) for k, v in map_stats.items()}

	# Calculate winrates
	for map_type, stats in map_stats.items():
		map_stats[map_type]['winrate'] = stats['wins'] / stats['total'] * 100

	# order the map_stats dictionary by map_type
	map_stats = dict(sorted(map_stats.items(), key=lambda item: item[0]))
	
	return map_stats