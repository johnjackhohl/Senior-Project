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
		'subMaps': subMaps
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
		'maps': maps
	}
	return render(request, 'match_inputs/Add_Push_Map.html', context)

def Add_Flashpoint(request, pk):
	game = models.Game.objects.get(id=pk)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	maps = models.Map.objects.filter(map_type="Flashpoint")
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
		'maps': maps
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
	roster = models.Roster.objects.filter(ow_team_id=game.match_id.ow_team_id.id)
	tanks = models.Hero.objects.filter(role="Tank")
	dps = models.Hero.objects.filter(role="DPS")
	support = models.Hero.objects.filter(role="Support")
	# take out when js is put in
	heroes = tanks | dps | support
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
		'tanks': tanks,
		'dps': dps,
		'support': support,
		'game': game,
		'heroes': heroes,
	}
	return render(request, 'match_inputs/Add_Game_Player.html', context)