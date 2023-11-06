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
			mapType = form.cleaned_data["map_type"]
			mapName = form.cleaned_data["map_name"]
			file_path = f"Overwatch_2/options/{mapType}_Maps.txt"
			with open(file_path, "r") as map_options:
				maps = [line.strip() for line in map_options]
			maps.remove(mapName)
			with open(file_path, "w") as map_options:
				for cnt, map in enumerate(maps):
					if cnt > 0:
						map_options.write("\n")
					map_options.write(map)
			if(mapType == "Control"):
				removeArray = []
				with open("OverWatch_2\options\Control_Sub_Maps.txt", "r") as map_sub_options:
					subMaps = [line.strip() for line in map_sub_options]
				for subMap in subMaps:
					if(mapName in subMap):
						removeArray.append(subMap)
				for subMap in removeArray:
					subMaps.remove(subMap)
				with open("OverWatch_2\options\Control_Sub_Maps.txt", "w") as map_sub_options:
					for cnt, subMap in enumerate(subMaps):
						if cnt > 0:
							map_sub_options.write("\n")
						map_sub_options.write(subMap)
			
			return redirect('rosters')
	else:
		form = forms.Delete_Map_Form()
		mapTypes = ["Escort", "Hybrid", "Push", "Flashpoint", "Control"]
		escortMaps = getMaps("Escort")
		hybridMaps = getMaps("Hybrid")
		pushMaps = getMaps("Push")
		flashpointMaps = getMaps("Flashpoint")
		controlMaps, controlSubMaps = getMaps("Control")
		maps = escortMaps + hybridMaps + pushMaps + flashpointMaps + controlMaps
		context = {
			'form': form,
			'mapTypes': mapTypes,
			'maps' : maps
		}
	return render(request, 'delete_templates/Delete_Map.html', context)

def Delete_Match_Type(request):
	if request.method == "POST":
		form = forms.Delete_Match_Type_Form(request.POST)
		if form.is_valid():
			matchType = form.cleaned_data["match_type"]
			with open("OverWatch_2\options\Match_Type.txt", "r") as match_options:
				matchTypes = [line.strip() for line in match_options]
			matchTypes.remove(matchType)
			with open("OverWatch_2\options\Match_Type.txt", "w") as match_options:
				for cnt, match in enumerate(matchTypes):
					if cnt > 0:
						match_options.write("\n")
					match_options.write(match)
			return redirect('rosters')
	else:
		form = forms.Delete_Match_Type_Form()
		with open("OverWatch_2\options\Match_Type.txt", "r") as match_options:
			matchTypes = [line.strip() for line in match_options]
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