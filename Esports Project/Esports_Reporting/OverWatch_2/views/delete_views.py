from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from OverWatch_2.helpers.input_helpers import getHeros, getMaps

def Delete_Hero(request):
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
		return render(request, 'delete_templates/Delete_Hero.html', context)

def Delete_Map(request):
	if request.method == "POST":
		form = forms.Delete_Map_Form(request.POST)
		if form.is_valid():
			map = models.Map.objects.get(map_name=form.cleaned_data["map_name"])
			if map.map_type == "Control":
				subMaps = models.Sub_Map.objects.filter(map_id=map.id)
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
	return render(request, 'delete_templates/Delete_Map.html', context)

def Delete_Match_Type(request):
	if request.method == "POST":
		form = forms.Delete_Match_Type_Form(request.POST)
		if form.is_valid():
			matchType = models.Match_Type.objects.get(match_type=form.cleaned_data["match_type"]).delete()
			return redirect('rosters')
	else:
		form = forms.Delete_Match_Type_Form()
		matchTypes = models.Match_Type.objects.all()
		context = {
			'form': form,
			'matchTypes': matchTypes
		}
	return render(request, 'delete_templates/Delete_Match_Type.html', context)

def Delete_Roster_Player(request, pk):
	player = models.Roster.objects.get(id=pk)
	team = models.OW_Team.objects.get(id=player.ow_team_id.id)
	player.delete()
	return redirect('team-roster', pk=team.id)

def delete_team_info(request, pk):
	team = models.OW_Team.objects.get(id=pk)
	team.delete()
	return redirect('rosters')

def delete_match(request, pk):
    match = models.Match.objects.get(id=pk)
    team = models.OW_Team.objects.get(id=match.ow_team_id.id)
    match.delete()
    return redirect('team-roster', pk=team.id)

def delete_game(request, pk):
    game = models.Game.objects.get(id=pk)
    team = models.OW_Team.objects.get(id=game.match_id.ow_team_id.id)
    game.delete()
    return redirect('team-roster', pk = team.id)

def delete_map(request, mapType, pk):
    if mapType in ['Escort', 'Hybrid']:
        if mapType == 'Escort':
            map = models.Escort_Hybrid_Map.objects.get(id=pk)
        else:
            map = models.Escort_Hybrid_Map.objects.get(id=pk)
    elif mapType == 'Control':
        map = models.Control_Map.objects.get(id=pk)
    elif mapType == 'Push':
        map = models.Push_Map.objects.get(id=pk)
    else:
        map = models.Flashpoint_Map.objects.get(id=pk) 
    team = models.OW_Team.objects.get(id=map.game_id.match_id.ow_team_id.id) 
    map.delete()
    return redirect('team-roster', pk=team.id)

def delete_player(request, pk):
    player = models.Player.objects.get(id=pk)
    team = models.OW_Team.objects.get(id=player.roster_id.ow_team_id.id)
    player.delete()
    return redirect('team-roster', pk=team.id)