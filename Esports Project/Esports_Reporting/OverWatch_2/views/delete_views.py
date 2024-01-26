from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models

def delete_hero(request):
	"""Deletes a hero from the database.

	Args:
		request

	Returns:
		render: returns a rendred html page with a form to delete a hero from the database
	"""
	if request.method == "POST":
		form = forms.Delete_Hero_Form(request.POST)
		if form.is_valid():
			hero = models.Hero.objects.get(hero_name=form.cleaned_data["hero_name"])
			hero.hero_image.delete()
			hero.delete()
			return redirect('rosters')
	else:
		form = forms.Delete_Hero_Form()
		heroes = models.Hero.objects.all()
		heroes = [hero.hero_name for hero in heroes]
		context = {
			'form': form,
			'heroes': heroes
		}
		return render(request, 'delete_templates/delete_hero.html', context)

def delete_map_name(request):
	"""Deletes a map from the database.

	Args:
		request

	Returns:
		render: returns a rendred html page with a form to delete a map from the database
	"""
	if request.method == "POST":
		form = forms.Delete_Map_Form(request.POST)
		if form.is_valid():
			map = models.Map.objects.get(map_name=form.cleaned_data["map_name"])
			if map.map_type == "Control":
				subMaps = models.SubMap.objects.filter(map_id=map.id)
				for subMap in subMaps:
					subMap.delete()
			map.map_image.delete()
			map.delete()
			return redirect('rosters')
	else:
		form = forms.Delete_Map_Form()
		maps = models.Map.objects.all()
		context = {
			'form': form,
			'maps' : maps
		}
	return render(request, 'delete_templates/delete_map.html', context)

def delete_match_type(request):
	"""Deletes a match type from the database.

	Args:
		request

	Returns:
		render: returns a rendred html page with a form to delete a match type from the database
	"""
	if request.method == "POST":
		form = forms.Delete_Match_Type_Form(request.POST)
		if form.is_valid():
			models.MatchType.objects.get(match_type=form.cleaned_data["match_type"]).delete()
			return redirect('rosters')
	else:
		form = forms.Delete_Match_Type_Form()
		matchTypes = models.MatchType.objects.all()
		context = {
			'form': form,
			'matchTypes': matchTypes
		}
	return render(request, 'delete_templates/delete_match_type.html', context)

def delete_roster_player(response, pk):
	"""Deletes a player from a roster.

	Args:
		response
		pk (int): primary key of the player to delete

	Returns:
		redirect: sends the user to the team roster page of the team that the player was deleted from
	"""
	player = models.Roster.objects.get(id=pk)
	player.is_active = False
	player.save()
	team = models.OwTeam.objects.get(id=player.ow_team_id.id)
	return redirect('team-roster', pk=team.id)

def delete_team(response, pk):
	"""Deletes a team from the database.

	Args:
		response
		pk (int): primary key of the team to delete

	Returns:
		redirect: sends the user to the team roster page of the team that was deleted
	"""
	team = models.OwTeam.objects.get(id=pk)
	team.delete()
	return redirect('rosters')

def delete_match(response, pk):
	"""Deletes a match from the database.

	Args:
		response
		pk (int): primary key of the match to delete

	Returns:
		redirect: sends the user to the team roster page of the team that the match was deleted from
	"""
	match = models.Match.objects.get(id=pk)
	team = models.OwTeam.objects.get(id=match.ow_team_id.id)
	match.delete()
	return redirect('team-roster', pk=team.id)

def delete_game(response, pk):
	"""Deletes a game from the database.

	Args:
		response
		pk (int): primary key of the game to delete

	Returns:
		redirect: sends the user to the team roster page of the team that the game was deleted from
	"""
	game = models.Game.objects.get(id=pk)
	team = models.OwTeam.objects.get(id=game.match_id.ow_team_id.id)
	game.delete()
	return redirect('team-roster', pk = team.id)

def delete_map(response, mapType, pk):
	"""Deletes a map from the database.

	Args:
		mapType (string): a string of the map type
		pk (int): primary key of the map to delete

	Returns:
		redirect: sends the user to the team roster page of the team that the map was deleted from
	"""
	if mapType in ['Escort', 'Hybrid']:
		if mapType == 'Escort':
			map = models.EscortHybridMap.objects.get(id=pk)
		else:
			map = models.EscortHybridMap.objects.get(id=pk)
	elif mapType == 'Control':
		map = models.ControlMap.objects.get(id=pk)
	elif mapType == 'Push':
		map = models.PushMap.objects.get(id=pk)
	elif mapType == 'Clash':
		map = models.ClashMap.objects.get(id=pk)
	else:
		map = models.FlashpointMap.objects.get(id=pk) 
	team = models.OwTeam.objects.get(id=map.game_id.match_id.ow_team_id.id) 
	map.delete()
	return redirect('team-roster', pk=team.id)

def delete_player(response, pk):
	"""Deletes a player from the database.

	Args:
		response
		pk (int): primary key of the player to delete

	Returns:
		redirect: sends user to the team roster page of the team that the player was deleted from
	"""
	player = models.Player.objects.get(id=pk)
	team = models.OwTeam.objects.get(id=player.roster_id.ow_team_id.id)
	player.delete()
	return redirect('team-roster', pk=team.id)