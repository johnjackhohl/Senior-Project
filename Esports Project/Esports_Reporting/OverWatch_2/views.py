from django.shortcuts import render, redirect
from datetime import datetime
from .forms import OW_Team_Form, Roster_Form, Match_Form, Game_Form, Control_Map_Form, Escort_Hybrid_Map_Form, Push_Map_Form, Flashpoint_Map_Form, Player_Form
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
	print(mapType)
	if(mapType == "Escort"):
		with open("OverWatch_2\options\Escort_Maps.txt", "r") as map_options:
			maps = [line.strip() for line in map_options]
		return maps
	if(mapType == "Hybrid"):
		with open("OverWatch_2\options\Hybrid_Maps.txt", "r") as map_options:
			maps = [line.strip() for line in map_options]
		return maps
	if(mapType == "Push"):
		with open("OverWatch_2\options\Push_Maps.txt", "r") as map_options:
			maps = [line.strip() for line in map_options]
		return maps
	if(mapType == "Flashpoint"):
		with open("OverWatch_2\options\Flashpoint_Maps.txt", "r") as map_options:
			maps = [line.strip() for line in map_options]
		return maps
	if(mapType == "Control"):
		with open("OverWatch_2\options\Control_Maps.txt", "r") as map_options:
			maps = [line.strip() for line in map_options]
		with open("OverWatch_2\options\Control_Sub_Maps.txt", "r") as map_sub_options:
			subMaps = [line.strip() for line in map_sub_options]
		return maps, subMaps
	