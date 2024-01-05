from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models

# Create your views here.
def OW_Rosters(request):
	OW_Teams = forms.OW_Team.objects.all()
	return render(request, 'team_templates/OW_Rosters.html', {"OW_Teams": OW_Teams})

def OW_Team_Roster(request, pk):
	team, owMatches = Match_History(pk)
	players = models.Roster.objects.filter(ow_team_id=team.id)
	heroPictures = models.Hero.objects.all()
	mapPictures = models.Map.objects.all()

	view = {
		"OW_Team": team,
		"Roster": players,
		"Hero_Pictures": heroPictures,
		"Matches": owMatches,
		"Map_Pictures": mapPictures
	}
	return render(request, 'team_templates/OW_Roster_Players.html', view)

def Match_History(pk):
	team = models.OW_Team.objects.get(id=pk)
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
				elif game.map_type == "Flashpoint":
					players = map.flashpoint_players.all()
				
				game_maps_with_players.append({
					'map': map,
					'players': players
				})

			# Attach this list to the game object
			game.maps_with_players = game_maps_with_players

	return team, owMatches