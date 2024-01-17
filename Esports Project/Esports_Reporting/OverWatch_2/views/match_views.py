import json
from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from django.forms import formset_factory

def Add_Match(request, pk):
	team = models.OW_Team.objects.get(id=pk)
	matchTypes = models.Match_Type.objects.all()
	if request.method == "POST":
		form = forms.Match_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-game', pk=form.instance.id)
	else:
		form = forms.Match_Form()
	return render(request, 'match_inputs/Add_Match.html', {'form': form, 'team': team, 'matchTypes': matchTypes})

def Add_Game(request, pk):
	match = models.Match.objects.get(id=pk)
	team = models.OW_Team.objects.get(id=match.ow_team_id.id)
	if request.method == "POST":
		form = forms.Game_Form(request.POST)
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
		form = forms.Game_Form()
	return render(request, 'match_inputs/Add_Game.html', {'form': form, 'match': match, 'team': team})

def Add_Control(request, pk):
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Control")
	subMaps = models.Sub_Map.objects.all()
	sub_maps = {map.map_name: list(map.sub_map_set.values('sub_map_name')) for map in maps}

	if request.method == "POST":
		form = forms.Control_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player',  mapType=game.map_type, pk=form.instance.id)
	else:
		form = forms.Control_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'subMaps': json.dumps(sub_maps),
	}
	return render(request, 'match_inputs/Add_Control_Map.html', context)

def Add_Escort_Hybrid(request, pk):
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	is_Escort = False
	if(game.map_type == "Escort"):
		is_Escort = True
		maps = models.Map.objects.filter(map_type="Escort")
	elif(game.map_type == "Hybrid"):
		maps = models.Map.objects.filter(map_type="Hybrid")
	
	if request.method == "POST":
		form = forms.Escort_Hybrid_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=form.instance.id, mapType=game.map_type)
	else:
		form = forms.Escort_Hybrid_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'is_Escort': is_Escort
	}
	return render(request, 'match_inputs/Add_Escort_Hybrid_Map.html', context)

def Add_Push(request, pk):
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Push")
	team = models.OW_Team.objects.get(id=game.match_id.ow_team_id.id)
	if request.method == "POST":
		form = forms.Push_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=form.instance.id, mapType=game.map_type)
	else:
		form = forms.Push_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'team': team
	}
	return render(request, 'match_inputs/Add_Push_Map.html', context)

def Add_Flashpoint(request, pk):
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Flashpoint")
	team = models.OW_Team.objects.get(id=game.match_id.ow_team_id.id)
	if request.method == "POST":
		form = forms.Flashpoint_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=form.instance.id, mapType=game.map_type)
	else:
		form = forms.Flashpoint_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'team': team
	}
	return render(request, 'match_inputs/Add_Flashpoint_Map.html', context)

def Add_Player(request, pk, mapType):
	PlayerFormSet = formset_factory(forms.Player_Form, extra=0)
	if mapType == "Control":
		map = models.Control_Map.objects.get(id=pk)
	elif mapType in ["Escort", "Hybrid"]:
		map = models.Escort_Hybrid_Map.objects.get(id=pk)
	elif mapType == "Push":
		map = models.Push_Map.objects.get(id=pk)
	elif mapType == "Flashpoint":
		map = models.Flashpoint_Map.objects.get(id=pk)
	game = models.Game.objects.get(id=map.game_id.id)
	roster = models.Roster.objects.filter(ow_team_id=game.match_id.ow_team_id.id, is_active=True)
	tanks, dps, support = getHeroes(map, mapType)
	rosterData = {player.id: player.role for player in roster}
	if game.map_type in ['Escort', 'Hybrid']:
		initial_data = [{'is_defense': False} for _ in range(5)] + [{'is_defense': True} for _ in range(5)]
	else:
		initial_data = [{'is_defense': False} for _ in range(5)]
	if request.method == "POST":
		formset = PlayerFormSet(request.POST, prefix='player', initial=initial_data)
		if formset.is_valid():
			for form in formset:
				player = form.save(commit=False)
				if mapType == "Control":
					player.control_id = map
				elif mapType in ["Escort", "Hybrid"]:
					player.escort_hybrid_id = map
				elif mapType == "Push":
					player.push_id = map
				elif mapType == "Flashpoint":
					player.flashpoint_id = map
				player.save()

			if request.POST.get('action') == "add_control":
				return redirect('add-control', pk=game.id)
			elif request.POST.get('action') == "add_flashpoint":
				return redirect('add-flashpoint', pk=game.id)
			else:
				return redirect('add-game', pk=game.match_id.id)
		else:
			print(formset.errors)
	else:
		formset = PlayerFormSet(prefix='player', initial=initial_data)

	context = {
		'formset': formset,
		'map': map,
		'roster': roster,
		'game': game,
		'supportData': json.dumps(support),
		'dpsData': json.dumps(dps),
		'tankData': json.dumps(tanks),
		'rosterData': json.dumps(rosterData),
	}
	return render(request, 'match_inputs/Add_Game_Player.html', context)

def add_single_player(request, mapType, pk):
	if mapType == "Control":
		map = models.Control_Map.objects.get(id=pk)
	elif mapType in ["Escort", "Hybrid"]:
		map = models.Escort_Hybrid_Map.objects.get(id=pk)
	elif mapType == "Push":
		map = models.Push_Map.objects.get(id=pk)
	elif mapType == "Flashpoint":
		map = models.Flashpoint_Map.objects.get(id=pk)
	game = models.Game.objects.get(id=map.game_id.id)
	roster = models.Roster.objects.filter(ow_team_id=game.match_id.ow_team_id.id)
	tanks, dps, support = getHeroes(map, mapType)
	rosterData = {player.id: player.role for player in roster}
	if request.method == "POST":
		form = forms.Player_Form(request.POST)
		if form.is_valid():
			player = form.save(commit=False)
			if mapType == "Control":
				player.control_id = map
			elif mapType in ["Escort", "Hybrid"]:
				player.escort_hybrid_id = map
			elif mapType == "Push":
				player.push_id = map
			elif mapType == "Flashpoint":
				player.flashpoint_id = map
			player.save()
			return redirect('team-roster', pk=map.game_id.match_id.ow_team_id.id)
		else:
			print(form.errors)
	else:
		form = forms.Player_Form()
	context = {
		'form': form,
		'map': map,
		'roster': roster,
		'game': game,
		'supportData': json.dumps(list(support)),
		'dpsData': json.dumps(list(dps)),
		'tankData': json.dumps(list(tanks)),
		'rosterData': json.dumps(rosterData),
	}
	return render(request, 'match_inputs/Add_Single_Player.html', context)

def getHeroes(map, mapType):
    tanks = []
    dps = []
    support = []
    if mapType in ["Escort", "Hybrid"]:
        AttackTank = map.mount_attack_tank
        defenseTank = map.mount_defense_tank
        
        attackDPS1 = map.mount_attack_dps_1
        attackDPS2 = map.mount_attack_dps_2
        defenseDPS1 = map.mount_defense_dps_1
        defenseDPS2 = map.mount_defense_dps_2
        
        attackSupport1 = map.mount_attack_support_1
        attackSupport2 = map.mount_attack_support_2
        defenseSupport1 = map.mount_defense_support_1
        defenseSupport2 = map.mount_defense_support_2
        
        tanks.append(AttackTank)
        tanks.append(defenseTank)
        
        dps.append(attackDPS1)
        dps.append(attackDPS2)
        dps.append(defenseDPS1)
        dps.append(defenseDPS2)
        
        support.append(attackSupport1)
        support.append(attackSupport2)
        support.append(defenseSupport1)
        support.append(defenseSupport2)
    else:
        tank = map.mount_tank
        dps1 = map.mount_dps_1
        dps2 = map.mount_dps_2
        support1 = map.mount_support_1
        support2 = map.mount_support_2
        
        tanks.append(tank)
        dps.append(dps1)
        dps.append(dps2)
        support.append(support1)
        support.append(support2)
    return tanks, dps, support