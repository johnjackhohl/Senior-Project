import json
from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from django.forms import formset_factory

def add_match(request, pk):
	"""Adds a match to the database

	Args:
		request
		pk (int): primary key of the team that the match is being added for

	Returns:
		render: returns a rendered html page with the form for adding a match
	"""
	team = models.OwTeam.objects.get(id=pk)
	matchTypes = models.MatchType.objects.all()
	if request.method == "POST":
		form = forms.Match_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-game', pk=form.instance.id)
	else:
		form = forms.Match_Form()
	return render(request, 'match_inputs/Add_Match.html', {'form': form, 'team': team, 'matchTypes': matchTypes})

def add_game(request, pk):
	"""Adds a game to the database

	Args:
		request
		pk (int): primary key of the match that the game is being added for

	Returns:
		render: returns a rendered html page with the form for adding a game 
	"""
	match = Match.objects.get(id=pk)
	team = models.OwTeam.objects.get(id=match.ow_team_id.id)
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
			if(mapType=="Clash"):
				return redirect('add-clash', pk=form.instance.id)
			
	else:
		form = forms.Game_Form()
	return render(request, 'match_inputs/Add_Game.html', {'form': form, 'match': match, 'team': team})

def add_control(request, pk):
	"""Adds a control map to the database

	Args:
		request
		pk (int): primary key of the game that the control map is being added for

	Returns:
		render: returns a rendered html page with the form for adding a control map
	"""
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Control")
	subMaps = models.SubMap.objects.all()
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

def add_escort_hybrid(request, pk):
	"""Adds a escort or hybrid map to the database

	Args:
		request
		pk (int): primary key of the game that the escort or hybrid map is being added for

	Returns:
		render: returns a rendered html page with the form for adding a escort or hybrid map
	"""
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

def add_push(request, pk):
	"""Adds a push map to the database

	Args:
		request
		pk (int): primary key of the game that the push map is being added for

	Returns:
		render: returns a rendered html page with the form for adding a push map
	"""
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Push")
	team = models.OwTeam.objects.get(id=game.match_id.ow_team_id.id)
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

def add_flashpoint(request, pk):
	"""Adds a flashpoint map to the database

	Args:
		request
		pk (int): primary key of the game that the flashpoint map is being added for

	Returns:
		render: returns a rendered html page with the form for adding a flashpoint map
	"""
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Flashpoint")
	team = models.OwTeam.objects.get(id=game.match_id.ow_team_id.id)
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

def add_clash(request, pk):
	"""Adds a clash map to the database

	Args:
		request
		pk (int): primary key of the game that the clash map is being added for

	Returns:
		render: returns a rendered html page with the form for adding a clash map
	"""
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Clash")
	team = models.OwTeam.objects.get(id=game.match_id.ow_team_id.id)
	if request.method == "POST":
		form = forms.Clash_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-player', pk=form.instance.id, mapType=game.map_type)
	else:
		form = forms.Clash_Map_Form()
	context = {
		'form': form,
		'game': game,
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'maps': maps,
		'team': team
	}
	return render(request, 'match_inputs/Add_Clash_Map.html', context)

def add_player(request, pk, mapType):
	"""Adds players to the database for a specific map, either 5 or 10 players depending on the map type

	Args:
		request
		pk (int): primary key of the map that the player is being added for
		mapType (string): string of the map type the player is being added too

	Returns:
		render: returns a rendered html page with the form for adding a player
	"""
	PlayerFormSet = formset_factory(forms.Player_Form, extra=0)
	if mapType == "Control":
		map = models.ControlMap.objects.get(id=pk)
	elif mapType in ["Escort", "Hybrid"]:
		map = models.EscortHybridMap.objects.get(id=pk)
	elif mapType == "Push":
		map = models.PushMap.objects.get(id=pk)
	elif mapType == "Flashpoint":
		map = models.FlashpointMap.objects.get(id=pk)
	elif mapType == "Clash":
		map = models.ClashMap.objects.get(id=pk)
	game = models.Game.objects.get(id=map.game_id.id)
	roster = models.Roster.objects.filter(ow_team_id=game.match_id.ow_team_id.id, is_active=True)
	tanks, dps, support = get_heroes(map, mapType)
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
				elif mapType == "Clash":
					player.clash_id = map
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
	"""Adds a single player to the database for a specific map

	Args:
		request
		mapType (string): string of the map type the player is being added too 
		pk (int): primary key of the map that the player is being added for

	Returns:
		render: returns a rendered html page with the form for adding a player
	"""
	if mapType == "Control":
		map = models.ControlMap.objects.get(id=pk)
	elif mapType in ["Escort", "Hybrid"]:
		map = models.EscortHybridMap.objects.get(id=pk)
	elif mapType == "Push":
		map = models.PushMap.objects.get(id=pk)
	elif mapType == "Flashpoint":
		map = models.FlashpointMap.objects.get(id=pk)
	game = models.Game.objects.get(id=map.game_id.id)
	roster = models.Roster.objects.filter(ow_team_id=game.match_id.ow_team_id.id)
	tanks, dps, support = get_heroes(map, mapType)
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

def get_heroes(map, mapType):
	"""Gets the heroes for a specific map

	Args:
		map (model): python model of the map that the heroes are being retrieved for
		mapType (string): string of the map type the heroes are being retrieved for

	Returns:
		tanks (list): list of the tank heroes for the map
		dps (list): list of the dps heroes for the map
		support (list): list of the support heroes for the map
	"""
	tanks = []
	dps = []
	support = []
	if mapType in ["Escort", "Hybrid"]:
		attackTank = map.mount_attack_tank
		defenseTank = map.mount_defense_tank
		
		attackDPS1 = map.mount_attack_dps_1
		attackDPS2 = map.mount_attack_dps_2
		defenseDPS1 = map.mount_defense_dps_1
		defenseDPS2 = map.mount_defense_dps_2
		
		attackSupport1 = map.mount_attack_support_1
		attackSupport2 = map.mount_attack_support_2
		defenseSupport1 = map.mount_defense_support_1
		defenseSupport2 = map.mount_defense_support_2
		
		tanks.append(attackTank)
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

