from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from OverWatch_2.helpers.input_helpers import getHeros, getMaps
from OverWatch_2.helpers.delete_helpers import deleteTeam

def Delete_Hero(request):
	if request.method == "POST":
		form = forms.Delete_Hero_Form(request.POST)
		if form.is_valid():
			role = form.cleaned_data["role"]
			heroName = form.cleaned_data["hero_name"]
			file_path = f"Overwatch_2/options/{role}.txt"
			with open(file_path, "r") as hero_options:
				heros = [line.strip() for line in hero_options]
			heros.remove(heroName)
			with open(file_path, "w") as hero_options:
				for cnt, hero in enumerate(heros):
					if cnt > 0:
						hero_options.write("\n")
					hero_options.write(hero)
			return redirect('rosters')
	else:
		form = forms.Delete_Hero_Form()
		[tanks, dps, support] = getHeros()
		heroes = tanks + dps + support
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
	if request.method == "POST":
		form = forms.Delete_Roster_Player_Form(request.POST)
		if form.is_valid():
			playerId = form.cleaned_data["player_id"]
			player = models.Roster.objects.get(id=playerId, ow_team_id=pk)
			print(player)
			player.delete()
			return redirect('team-roster', pk=pk)
	else:
		form = forms.Delete_Roster_Player_Form()
		roster = models.Roster.objects.filter(ow_team_id=pk)
		context = {
			'form': form,
			'roster': roster,
			'pk': pk
		}
	return render(request, 'delete_templates/Delete_Roster_Player.html', context)

def delete_team_info(request, pk):
	deleteTeam(pk)
	return redirect('rosters')