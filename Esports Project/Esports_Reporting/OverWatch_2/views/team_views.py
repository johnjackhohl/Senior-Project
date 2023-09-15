from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models


# Create your views here.
def OW_Rosters(request):
	OW_Teams = forms.OW_Team.objects.all()
	return render(request, 'team_templates/OW_Rosters.html', {"OW_Teams": OW_Teams})

def OW_Team_Roster(request, pk):
    team, players, owMatches = Match_History(pk)
    view = {
		"OW_Team": team,
		"Roster": players,
		"Matches": owMatches
	}
    return render(request, 'team_templates/OW_Roster_Players.html', view)

def Match_History(pk):
	team = models.OW_Team.objects.get(id=pk)
	players = models.Roster.objects.filter(ow_team_id=pk)
	owMatches = models.Match.objects.filter(ow_team_id=pk)
	for match in owMatches:
		games_related_to_match = models.Game.objects.filter(match_id=match.id)
		match.games = games_related_to_match
    	
		for game in games_related_to_match:
			game.players = models.Player.objects.filter(game_id=game.id)

			if game.map_type == "Control":
				game.maps = models.Control_Map.objects.filter(game_id=game.id)
			elif game.map_type in ["Escort", "Hybrid"]:
				game.maps = models.Escort_Hybrid_Map.objects.filter(game_id=game.id)
			elif game.map_type == "Push":
				game.maps = models.Push_Map.objects.filter(game_id=game.id)
			else:
				game.maps = models.Flashpoint_Map.objects.filter(game_id=game.id)
	return team, players, owMatches









