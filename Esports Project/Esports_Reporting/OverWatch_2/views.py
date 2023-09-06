from django.shortcuts import render, redirect
from datetime import datetime
from .forms import OW_Team_Form, Roster_Form, Match_Form, Game_Form, Control_Map_Form, Escort_Hybrid_Map_Form, Push_Map_Form 
from .forms import Flashpoint_Map_Form, Player_Form, Add_Hero_Form, Add_Map_Form, Add_Control_Sub_Map_Form, Add_Hero_Form, Delete_Hero_Form, Delete_Map_Form
from .models import OW_Team, Roster, Match, Game


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
	view = {
		"OW_Team": team,
		"Roster": players
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
	return render(request, 'Add_Game.html', {'form': form, 'match': match})

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
			redirect('add-player', pk=game.id)
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
			if(role == "Tank"):
				with open("OverWatch_2\options\Tank.txt", "a") as tank_options:
					tank_options.write("\n" + heroName)
			if(role == "DPS"):
				with open("OverWatch_2\options\DPS.txt", "a") as dps_options:
					dps_options.write("\n" + heroName)
			if(role == "Support"):
				with open("OverWatch_2\options\Support.txt", "a") as support_options:
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
			if(mapType == "Escort"):
				with open("OverWatch_2\options\Escort_Maps.txt", "a") as map_options:
					map_options.write("\n" + mapName)
			if(mapType == "Hybrid"):
				with open("OverWatch_2\options\Hybrid_Maps.txt", "a") as map_options:
					map_options.write("\n" + mapName)
			if(mapType == "Push"):
				with open("OverWatch_2\options\Push_Maps.txt", "a") as map_options:
					map_options.write("\n" + mapName)
			if(mapType == "Flashpoint"):
				with open("OverWatch_2\options\Flashpoint_Maps.txt", "a") as map_options:
					map_options.write("\n" + mapName)
			if(mapType == "Control"):
				with open("OverWatch_2\options\Control_Maps.txt", "a") as map_options:
					map_options.write("\n" + mapName)
				return redirect('add-sub-map', mapName)
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
				with open("OverWatch_2\options\Control_Sub_Maps.txt", "r") as map_sub_options:
					subMaps = [line.strip() for line in map_sub_options]
				for subMap in subMaps:
					if(mapName in subMap):
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