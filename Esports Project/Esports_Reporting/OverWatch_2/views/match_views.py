from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from OverWatch_2.helpers.input_helpers import getHeros, getMaps
from django.forms import formset_factory
import json

def Add_Match(request, pk):
	team = models.OW_Team.objects.get(id=pk)
	with open("OverWatch_2\options\Match_Type.txt", "r") as matchOptions:
		matchTypes = [line.strip() for line in matchOptions]
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
	[tanks, dps, support] = getHeros()
	maps, subMaps = getMaps(game.map_type)
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
	[tanks, dps, support] = getHeros()
	maps = getMaps(game.map_type)
	is_Escort = False
	if(game.map_type == "Escort"):
		is_Escort = True
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
	[tanks, dps, support] = getHeros()
	maps = getMaps(game.map_type)
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
	[tanks, dps, support] = getHeros()
	maps = getMaps(game.map_type)
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
	[tanks, dps, support] = getHeros()
	heroes = tanks + dps + support
	""" heroes = {
		"Tank": tanks,
		"DPS": dps,
		"Support": support
	} """
	if game.map_type in ['Escort', 'Hybrid']:
		initial_data = [{'is_defense': False} for _ in range(5)] + [{'is_defense': True} for _ in range(5)]
	else:
		initial_data = [{'is_defense': False} for _ in range(5)]
	if request.method == "POST":
		formset = PlayerFormSet(request.POST, prefix='player', initial=initial_data)
		if formset.is_valid():
			for form in formset:
				form.save()
			if request.POST.get('action') == "add_control":
				return redirect('add-control', pk=game.id)
			if request.POST.get('action') == "add_flashpoint":
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
		'heroes': heroes,
		'game': game
	}
	return render(request, 'match_inputs/Add_Game_Player.html', context)