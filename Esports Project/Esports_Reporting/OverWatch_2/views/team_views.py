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
	return render(request, 'team_templates/ow_rosters.html', {"OW_Teams": OW_Teams})

def ow_team_roster(request, pk):
	team, owMatches = match_history(pk)
	# get only players who is_active is True
	players = models.Roster.objects.filter(ow_team_id=team.id, is_active=True)
	# get one picture from each map type
	map_stats = map_winrates(pk)
	comps = top_comp(pk)
	opponent_comps = top_opponent_comps(pk)
	print(opponent_comps)
	view = {
		"OW_Team": team,
		"Roster": players,
		"Matches": owMatches,
		"Map_Stats": map_stats,
		"Comps": comps,
		"Opponent_Comps": opponent_comps
	}
	return render(request, 'team_templates/ow_team_roster.html', view)

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
		map_stats[map_type]['winrate'] = round((stats['wins'] / stats['total'] * 100),2)

	for type in ["Control", "Escort", "Hybrid", "Push", "Clash", "Flashpoint"]:
		if type in map_stats:
			map_image = models.Map.objects.filter(map_type=type).first()
			image_url = map_image.map_image.url if map_image else None
			map_stats[type]['image_url'] = image_url

	# order the map_stats dictionary by map_type
	map_stats = dict(sorted(map_stats.items(), key=lambda item: item[0]))
	
	return map_stats

def top_comps(pk):
	"""This function is used to get the most used compositions for a team, and the winrate for this composition.

	Args:
		pk (_type_): _description_
	"""

	games = models.Game.objects.filter(match_id__ow_team_id=pk)

	# This will be a dictionary of dictionaries
	comps = {}

	for game in games:
		mapType = game.map_type
		maps = game.get_maps()
		for map in maps:
			if mapType not in ["Escort", "Hybrid"]:
				# Sort the DPS and Support players to standardize the composition key
				dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
				support_players = sorted([map.mount_support_1, map.mount_support_2])
			
				# The composition key is now the tank, sorted DPS, and sorted support players
				comp_key = (map.mount_tank, tuple(dps_players), tuple(support_players))

				# Initialize the map type if not already present
				if mapType not in comps:
					comps[mapType] = {}

				# Initialize the specific composition if not already present
				if comp_key not in comps[mapType]:
					comps[mapType][comp_key] = {'wins': 0, 'total': 0, 'winrate': 0}

				# Increment the total and wins (if applicable)
				comps[mapType][comp_key]['total'] += 1
				if game.mount_win:
					comps[mapType][comp_key]['wins'] += 1
				
				# Update the win rate
				comps[mapType][comp_key]['winrate'] = round((comps[mapType][comp_key]['wins'] / comps[mapType][comp_key]['total']) * 100,2)
			else:
				# Sort the DPS and Support players to standardize the composition key
				attack_dps_players = sorted([map.mount_attack_dps_1, map.mount_attack_dps_2])
				attack_support_players = sorted([map.mount_attack_support_1, map.mount_attack_support_2])

				defense_dps_players = sorted([map.mount_defense_dps_1, map.mount_defense_dps_2])
				defense_support_players = sorted([map.mount_defense_support_1, map.mount_defense_support_2])

				attack_comp_key = (map.mount_attack_tank, tuple(attack_dps_players), tuple(attack_support_players))
				defense_comp_key = (map.mount_defense_tank, tuple(defense_dps_players), tuple(defense_support_players))

				# Initialize the map type if not already present
				if mapType not in comps:
					comps[mapType] = {}

				if attack_comp_key not in comps[mapType]:
					comps[mapType][attack_comp_key] = {'wins': 0, 'total': 0, 'winrate': 0}

				comps[mapType][attack_comp_key]['total'] += 1
				if game.mount_win and not map.attack_first:
					comps[mapType][attack_comp_key]['wins'] += 1

				comps[mapType][attack_comp_key]['winrate'] = round((comps[mapType][attack_comp_key]['wins'] / comps[mapType][attack_comp_key]['total']) * 100, 2)

				# Check and update for defense composition
				if defense_comp_key not in comps[mapType]:
					comps[mapType][defense_comp_key] = {'wins': 0, 'total': 0, 'winrate': 0}

				comps[mapType][defense_comp_key]['total'] += 1
				if game.mount_win and map.attack_first:
					comps[mapType][defense_comp_key]['wins'] += 1

				comps[mapType][defense_comp_key]['winrate'] = round((comps[mapType][defense_comp_key]['wins'] / comps[mapType][defense_comp_key]['total']) * 100, 2)
			
			# Sort the comps dictionary by map type
			comps = dict(sorted(comps.items(), key=lambda item: item[0]))

			# Sort the compositions for each map type by total games played
			for mapType, compDict in comps.items():
				comps[mapType] = dict(sorted(compDict.items(), key=lambda item: item[1]['total'], reverse=True))
	print(comps)
	# delete the comps that are not the first of each map type
	for mapType, compDict in comps.items():
		for comp in list(compDict)[1:]:
			del compDict[comp]
	return comps

def top_comp(pk):
	games = models.Game.objects.filter(match_id__ow_team_id=pk)

	# This will be a dictionary of dictionaries
	comps = {}

	for game in games:
		mapType = game.map_type
		maps = game.get_maps()
		for map in maps:
			if mapType not in ["Escort", "Hybrid"]:
				# For non-Escort and non-Hybrid maps
				dps_players = sorted([map.mount_dps_1, map.mount_dps_2])
				support_players = sorted([map.mount_support_1, map.mount_support_2])
				comp_key = (map.mount_tank, tuple(dps_players), tuple(support_players))

				if mapType not in comps:
					comps[mapType] = {}

				if comp_key not in comps[mapType]:
					comps[mapType][comp_key] = {'wins': 0, 'total': 0, 'winrate': 0}
				
				comps[mapType][comp_key]['total'] += 1
				if game.mount_win:
					comps[mapType][comp_key]['wins'] += 1
				comps[mapType][comp_key]['winrate'] = round((comps[mapType][comp_key]['wins'] / comps[mapType][comp_key]['total']) * 100,2)
			else:
				# For Escort and Hybrid maps
				for comp_type, is_defense in [('attack', False), ('defense', True)]:
					dps_players = sorted([getattr(map, f"mount_{comp_type}_dps_1"), getattr(map, f"mount_{comp_type}_dps_2")])
					support_players = sorted([getattr(map, f"mount_{comp_type}_support_1"), getattr(map, f"mount_{comp_type}_support_2")])
					comp_key = (getattr(map, f"mount_{comp_type}_tank"), tuple(dps_players), tuple(support_players), is_defense)
					
					if mapType not in comps:
						comps[mapType] = {}

					if comp_key not in comps[mapType]:
						comps[mapType][comp_key] = {'wins': 0, 'total': 0, 'winrate': 0, 'is_defense': is_defense}
					
					comps[mapType][comp_key]['total'] += 1
					if game.mount_win:
						comps[mapType][comp_key]['wins'] += 1
					comps[mapType][comp_key]['winrate'] = round((comps[mapType][comp_key]['wins'] / comps[mapType][comp_key]['total']) * 100,2)
	# Sorting and keeping only the top comp for each map type
	top_comps = {}
	for mapType, compDict in comps.items():
		sorted_comps = sorted(compDict.items(), key=lambda x: (-x[1]['total'], -x[1]['winrate']))
		if mapType in ["Escort", "Hybrid"]:
			# For Escort and Hybrid maps, we need to keep track of the attack and defense comps separately
			attack_comp = sorted([comp for comp in sorted_comps if not comp[1]['is_defense']], key=lambda x: (-x[1]['total'], -x[1]['winrate']))
			defense_comp = sorted([comp for comp in sorted_comps if comp[1]['is_defense']], key=lambda x: (-x[1]['total'], -x[1]['winrate']))
			top_comps[mapType] = {
				'attack': attack_comp[0] if attack_comp else None,
				'defense': defense_comp[0] if defense_comp else None
			}
		else:
			top_comps[mapType] = sorted_comps[0] if sorted_comps else None
	
	flattened_comps = {}
	for mapType, comp_info in top_comps.items():
		if mapType in ["Escort", "Hybrid"]:
			# Add attack and defense compositions separately
			if comp_info['attack']:
				attack_key = f"{mapType} (Attack)"
				attack_comp = comp_info['attack'][0]
				flattened_comps[attack_key] = {
					'tank': attack_comp[0],
					'dps': attack_comp[1],
					'support': attack_comp[2],
					'stats': comp_info['attack'][1]
				}
			if comp_info['defense']:
				defense_key = f"{mapType} (Defense)"
				defense_comp = comp_info['defense'][0]
				flattened_comps[defense_key] = {
					'tank': defense_comp[0],
					'dps': defense_comp[1],
					'support': defense_comp[2],
					'stats': comp_info['defense'][1]
				}
		else:
			if comp_info:
				comp = comp_info[0]
				flattened_comps[mapType] = {
					'tank': comp[0],
					'dps': comp[1],
					'support': comp[2],
					'stats': comp_info[1]
				}
	
	return flattened_comps

def top_opponent_comps(pk):
	"""This function is used to get the most used compositions for a team, and the winrate for this composition.

	Args:
		pk (int): primary key of the team to get compositions for

	Returns:
		dictonary: this dictionary contains the most used compositions for each map type, and the winrate for this composition, it is a defult dict wthin a 
		defult dict, within a dictionary
	"""
	games = models.Game.objects.filter(match_id__ow_team_id=pk)

	# This will be a dictionary of dictionaries
	comps = {}

	for game in games:
		mapType = game.map_type
		maps = game.get_maps()
		for map in maps:
			if mapType not in ["Escort", "Hybrid"]:
				# For non-Escort and non-Hybrid maps
				dps_players = sorted([map.opponent_dps_1, map.opponent_dps_2])
				support_players = sorted([map.opponent_support_1, map.opponent_support_2])
				comp_key = (map.opponent_tank, tuple(dps_players), tuple(support_players))

				if mapType not in comps:
					comps[mapType] = {}

				if comp_key not in comps[mapType]:
					comps[mapType][comp_key] = {'wins': 0, 'total': 0, 'winrate': 0}
				
				comps[mapType][comp_key]['total'] += 1
				if not game.mount_win:
					comps[mapType][comp_key]['wins'] += 1
				comps[mapType][comp_key]['winrate'] = round((comps[mapType][comp_key]['wins'] / comps[mapType][comp_key]['total']) * 100,2)
			else:
				# For Escort and Hybrid maps
				for comp_type, is_defense in [('attack', False), ('defense', True)]:
					dps_players = sorted([getattr(map, f"opponent_{comp_type}_dps_1"), getattr(map, f"opponent_{comp_type}_dps_2")])
					support_players = sorted([getattr(map, f"opponent_{comp_type}_support_1"), getattr(map, f"opponent_{comp_type}_support_2")])
					comp_key = (getattr(map, f"opponent_{comp_type}_tank"), tuple(dps_players), tuple(support_players), is_defense)
					
					if mapType not in comps:
						comps[mapType] = {}

					if comp_key not in comps[mapType]:
						comps[mapType][comp_key] = {'wins': 0, 'total': 0, 'winrate': 0, 'is_defense': is_defense}
					
					comps[mapType][comp_key]['total'] += 1
					if not game.mount_win:
						comps[mapType][comp_key]['wins'] += 1
					comps[mapType][comp_key]['winrate'] = round((comps[mapType][comp_key]['wins'] / comps[mapType][comp_key]['total']) * 100,2)
	# Sorting and keeping only the top comp for each map type
	top_comps = {}
	for mapType, compDict in comps.items():
		sorted_comps = sorted(compDict.items(), key=lambda x: (-x[1]['total'], -x[1]['winrate']))
		if mapType in ["Escort", "Hybrid"]:
			# For Escort and Hybrid maps, we need to keep track of the attack and defense comps separately
			attack_comp = sorted([comp for comp in sorted_comps if not comp[1]['is_defense']], key=lambda x: (-x[1]['total'], -x[1]['winrate']))
			defense_comp = sorted([comp for comp in sorted_comps if comp[1]['is_defense']], key=lambda x: (-x[1]['total'], -x[1]['winrate']))
			top_comps[mapType] = {
				'attack': attack_comp[0] if attack_comp else None,
				'defense': defense_comp[0] if defense_comp else None
			}
		else:
			top_comps[mapType] = sorted_comps[0] if sorted_comps else None
	
	flattened_comps = {}
	for mapType, comp_info in top_comps.items():
		if mapType in ["Escort", "Hybrid"]:
			# Add attack and defense compositions separately
			if comp_info['attack']:
				attack_key = f"{mapType} (Attack)"
				attack_comp = comp_info['attack'][0]
				flattened_comps[attack_key] = {
					'tank': attack_comp[0],
					'dps': attack_comp[1],
					'support': attack_comp[2],
					'stats': comp_info['attack'][1]
				}
			if comp_info['defense']:
				defense_key = f"{mapType} (Defense)"
				defense_comp = comp_info['defense'][0]
				flattened_comps[defense_key] = {
					'tank': defense_comp[0],
					'dps': defense_comp[1],
					'support': defense_comp[2],
					'stats': comp_info['defense'][1]
				}
		else:
			if comp_info:
				comp = comp_info[0]
				flattened_comps[mapType] = {
					'tank': comp[0],
					'dps': comp[1],
					'support': comp[2],
					'stats': comp_info[1]
				}
	
	return flattened_comps