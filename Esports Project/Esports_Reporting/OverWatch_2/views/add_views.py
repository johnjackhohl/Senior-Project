from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models
from django.forms import formset_factory

def Add_Player_to_Roster(request, pk):
	team = models.OW_Team.objects.get(id=pk)
	if request.method == "POST":
		form = forms.Roster_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('team-roster', pk=pk)
	else:
		form = forms.Roster_Form()
	return render(request, 'add_templates/Add_OW_Player.html', {'form': form, 'team': team})

def Create_OW_Team(request):
	if request.method == "POST":
		form = forms.OW_Team_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('rosters')
	else:
		form = forms.OW_Team_Form()
	return render(request, 'add_templates/Create_OW_Team.html', {'form': form})

def Add_Hero(request):
	if request.method == "POST":
		form = forms.Add_Hero_Form(request.POST, request.FILES)
		print(form)
		if form.is_valid():
			form.save()
			return redirect('rosters')
	else:
		form = forms.Add_Hero_Form()
	return render(request, 'add_templates/Add_Hero.html', {'form': form})	

def Add_Map(request):
	if request.method == "POST":
		form = forms.Add_Map_Form(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			mapType = form.cleaned_data["map_type"]
			if(mapType == "Control"):
				return redirect('add-sub-map', pk=form.instance.id)
			else:
				return redirect('rosters')
		if form.errors:
			print(form.errors)
			return redirect('rosters')
	else:
		form = forms.Add_Map_Form()
	return render(request, 'add_templates/Add_Map.html', {'form': form})

def Add_Sub_Map(request, pk):
	map_instance = models.Map.objects.get(id=pk)
	subMapFormset = formset_factory(forms.Add_Sub_Map, extra=0)
	
	if request.method == "POST":
		formset = subMapFormset(request.POST, request.FILES, prefix='subMap')
		if formset.is_valid():
			for form in formset:
				form.save()
			return redirect('rosters')
		if formset.errors:
			print(formset.errors)
	else:
		initial_data = [{'map_id': map_instance.id} for _ in range(3)]
		formset = subMapFormset(prefix='subMap', initial=initial_data) 

	
	context = {
		'formset': formset,
		'mapName': map_instance.map_name,
	}
	return render(request, 'add_templates/Add_Sub_Map.html', context)


def Add_Match_Type(request):
	if request.method == "POST":
		form = forms.Add_Match_Type_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('rosters')
	else:
		form = forms.Add_Match_Type_Form()
	return render(request, 'add_templates/Add_Match_Type.html', {'form': form})

def Add_Map_Type(request):
	if request.method == "POST":
		form = forms.Add_Map_Type_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('rosters')
	else:
		form = forms.Add_Map_Type_Form()
	return render(request, 'add_templates/Add_Map_Type.html', {'form': form})