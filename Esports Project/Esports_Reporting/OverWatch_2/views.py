from django.shortcuts import render, redirect
from .forms import *
from .models import OW_Team, Roster, Match, Game, Control_Map, Escort_Hybrid_Map, Flashpoint_Map, Push_Map, Player


# Create your views here.
def Create_OW_Team(request):
	if request.method == "POST":
		form = OW_Team_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('rosters')
	else:
		form = OW_Team_Form()
	return render(request, 'Create_OW_Team.html', {'form': form})

def Add_Player_to_Roster(request, pk):
	team = OW_Team.objects.get(id=pk)
	if request.method == "POST":
		form = Roster_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('roster-players', pk=pk)
	else:
		form = Roster_Form()
	return render(request, 'Add_OW_Player.html', {'form': form, 'team': team})
	

def OW_Roster(request):
	OW_Teams = OW_Team.objects.all()
	return render(request, 'OW_Rosters.html', {"OW_Teams": OW_Teams})

def OW_Roster_Players(request, pk):
	team = OW_Team.objects.get(id=pk)
	players = Roster.objects.filter(ow_team_id=pk)
	owMatches = Match.objects.filter(ow_team_id=pk)
	for match in owMatches:
		games_related_to_match = Game.objects.filter(match_id=match.id)
		match.games = games_related_to_match
    	
		for game in games_related_to_match:
			game.players = Player.objects.filter(game_id=game.id)

			if game.map_type == "Control":
				game.maps = Control_Map.objects.filter(game_id=game.id)
			elif game.map_type in ["Escort", "Hybrid"]:
				game.maps = Escort_Hybrid_Map.objects.filter(game_id=game.id)
			elif game.map_type == "Push":
				game.maps = Push_Map.objects.filter(game_id=game.id)
			else:
				game.maps = Flashpoint_Map.objects.filter(game_id=game.id)

	view = {
		"OW_Team": team,
		"Roster": players,
		"Matches": owMatches
	}
	return render(request, 'OW_Roster_Players.html', view)

def Add_Match(request, pk):
	team = OW_Team.objects.get(id=pk)
	with open("OverWatch_2\options\Match_Type.txt", "r") as matchOptions:
		matchTypes = [line.strip() for line in matchOptions]
	if request.method == "POST":
		form = Match_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-game', pk=form.instance.id)
	else:
		form = Match_Form()
	return render(request, 'Add_Match.html', {'form': form, 'team': team, 'matchTypes': matchTypes})

def Add_Game(request, pk):
	match = Match.objects.get(id=pk)
	team = OW_Team.objects.get(id=match.ow_team_id.id)
	if request.method == "POST":
		form = Game_Form(request.POST)
		if form.is_valid():
			mapType = form.cleaned_data["map_type"]
			form.save()
			if(mapType == "Control"):
				return redirect('add-control', pk=form.instance.id)
			if(mapType == "Escort" or mapType == "Hybrid"):
				return redirect('add-escort-hybrid', pk=form.instance.id)
			if(mapType=="Push"):
				return redirect('add-push', pk=form.instance.id)
			if(mapType=='Flashpoint'):
				return redirect('add-flashpoint', pk=form.instance.id)
	else:
		form = Game_Form()
	return render(request, 'Add_Game.html', {'form': form, 'match': match, 'team': team})

def Add_Control(request, pk):
	game = Game.objects.get(id=pk)
	[tanks, dps, support] = getHeros()
	maps, subMaps = getMaps(game.map_type)
	if request.method == "POST":
		form = Control_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=game.id)
	else:
		form = Control_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'subMaps': subMaps
	}
	return render(request, 'Add_Control_Map.html', context)

def Add_Escort_Hybrid(request, pk):
	game = Game.objects.get(id=pk)
	[tanks, dps, support] = getHeros()
	maps = getMaps(game.map_type)
	is_Escort = False
	if(game.map_type == "Escort"):
		is_Escort = True
	if request.method == "POST":
		form = Escort_Hybrid_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=game.id)
	else:
		form = Escort_Hybrid_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'is_Escort': is_Escort
	}
	return render(request, 'Add_Escort_Hybrid_Map.html', context)

def Add_Push(request, pk):
	game = Game.objects.get(id=pk)
	[tanks, dps, support] = getHeros()
	maps = getMaps(game.map_type)
	if request.method == "POST":
		form = Push_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=game.id)
	else:
		form = Push_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps
	}
	return render(request, 'Add_Push_Map.html', context)

def Add_Flashpoint(request, pk):
	game = Game.objects.get(id=pk)
	[tanks, dps, support] = getHeros()
	maps = getMaps(game.map_type)
	if request.method == "POST":
		form = Flashpoint_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=game.id)
	else:
		form = Flashpoint_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps
	}
	return render(request, 'Add_Flashpoint_Map.html', context)

def Add_Player(request, pk):
	game = Game.objects.get(id=pk)
	roster = Roster.objects.filter(ow_team_id=game.match_id.ow_team_id.id)
	[tanks, dps, support] = getHeros()
	heroes = tanks + dps + support
	if request.method == "POST":
		form = Player_Form(request.POST)
		if form.is_valid():
			if request.POST.get('action') == "add_another_player":
				form.save()
				return redirect('add-player', pk=pk)
			if request.POST.get('action') == "add_control":
				form.save()
				return redirect('add-control', pk=pk)
			if request.POST.get('action') == "add_flashpoint":
				form.save()
				return redirect('add-flashpoint', pk=pk)
			else:
				form.save()
				return redirect('add-game', pk=game.match_id.id)
	else:
		form = Player_Form()
	context = {
		'form': form,
		'game': game,
		'roster': roster,
		'heroes': heroes
	}
	return render(request, 'Add_Game_Player.html', context)

def getHeros():
	with open("OverWatch_2\options\Tank.txt", "r") as tank_options:
		tanks = [line.strip() for line in tank_options]
	with open("OverWatch_2\options\DPS.txt", "r") as dps_options:
		dps = [line.strip() for line in dps_options]
	with open("OverWatch_2\options\Support.txt", "r") as support_options:
		support = [line.strip() for line in support_options]
	return [tanks, dps, support]

def getMaps(mapType):
	file_path = f"Overwatch_2/options/{mapType}_Maps.txt"
	with open(file_path, "r") as map_options:
		maps = [line.strip() for line in map_options]
	if(mapType == "Control"):
		with open("OverWatch_2\options\Control_Sub_Maps.txt", "r") as map_sub_options:
			subMaps = [line.strip() for line in map_sub_options]
		return maps, subMaps
	else:
		return maps

def Add_Hero(request):
	if request.method == "POST":
		form = Add_Hero_Form(request.POST)
		if form.is_valid():
			role = form.cleaned_data["role"]
			heroName = form.cleaned_data["hero_name"]
			filePath = f"Overwatch_2/options/{role}.txt"
			with open(filePath, "a") as support_options:
				support_options.write("\n" + heroName)
			return redirect('rosters')
	else:
		form = Add_Hero_Form()
	return render(request, 'Add_Hero.html', {'form': form})	

def Add_Map(request):
	if request.method == "POST":
		form = Add_Map_Form(request.POST)
		if form.is_valid():
			mapType = form.cleaned_data["map_type"]
			mapName = form.cleaned_data["map_name"]
			filePath = f"Overwatch_2/options/{mapType}_Maps.txt"
			with open(filePath, "a") as map_options:
					map_options.write("\n" + mapName)
			if(mapType == "Control"):
				return redirect('add-sub-map', mapName)
			else:
				return redirect('rosters')
	else:
		form = Add_Map_Form()
	return render(request, 'Add_Map.html', {'form': form})

def Add_Sub_Map(request, mapName):
	if request.method == "POST":
		form = Add_Control_Sub_Map_Form(request.POST)
		if form.is_valid():
			mapSubName1 = form.cleaned_data["sub_map_1"]
			mapSubName2 = form.cleaned_data["sub_map_2"]
			mapSubName3 = form.cleaned_data["sub_map_3"]
			with open("OverWatch_2\options\Control_Sub_Maps.txt", "a") as map_sub_options:
				map_sub_options.write("\n" + mapName + ": " + mapSubName1)
				map_sub_options.write("\n" + mapName + ": " + mapSubName2)
				map_sub_options.write("\n" + mapName + ": " + mapSubName3)
			return redirect('rosters')
	else:
		form = Add_Control_Sub_Map_Form()
	return render(request, 'Add_Sub_Map.html', {'form': form, 'mapName': mapName})

def Delete_Hero(request):
	if request.method == "POST":
		form = Delete_Hero_Form(request.POST)
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
		form = Delete_Hero_Form()
		[tanks, dps, support] = getHeros()
		heroes = tanks + dps + support
		context = {
			'form': form,
			'heroes': heroes
		}
		return render(request, 'Delete_Hero.html', context)

def Delete_Map(request):
	if request.method == "POST":
		form = Delete_Map_Form(request.POST)
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
		form = Delete_Map_Form()
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
	return render(request, 'Delete_Map.html', context)

def Delete_Match_Type(request):
	if request.method == "POST":
		form = Delete_Match_Type_Form(request.POST)
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
		form = Delete_Match_Type_Form()
		with open("OverWatch_2\options\Match_Type.txt", "r") as match_options:
			matchTypes = [line.strip() for line in match_options]
		context = {
			'form': form,
			'matchTypes': matchTypes
		}
	return render(request, 'Delete_Match_Type.html', context)

def Add_Match_Type(request):
	if request.method == "POST":
		form = Add_Match_Type_Form(request.POST)
		if form.is_valid():
			matchType = form.cleaned_data["match_type"]
			with open("OverWatch_2\options\Match_Type.txt", "a") as match_options:
				match_options.write("\n" + matchType)
			return redirect('rosters')
	else:
		form = Add_Match_Type_Form()
	return render(request, 'Add_Match_Type.html', {'form': form})

def Delete_Roster_Player(request, pk):
	if request.method == "POST":
		form = Delete_Roster_Player_Form(request.POST)
		if form.is_valid():
			playerId = form.cleaned_data["player_id"]
			player = Roster.objects.get(id=playerId, ow_team_id=pk)
			print(player)
			player.delete()
			return redirect('roster-players', pk=pk)
	else:
		form = Delete_Roster_Player_Form()
		roster = Roster.objects.filter(ow_team_id=pk)
		context = {
			'form': form,
			'roster': roster,
			'pk': pk
		}
	return render(request, 'Delete_Roster_Player.html', context)