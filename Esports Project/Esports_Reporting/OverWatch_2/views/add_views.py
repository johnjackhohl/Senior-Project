from django.shortcuts import render, redirect
from OverWatch_2 import forms
from OverWatch_2 import models

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
		form = forms.Add_Hero_Form(request.POST)
		if form.is_valid():
			role = form.cleaned_data["role"]
			heroName = form.cleaned_data["hero_name"]
			filePath = f"Overwatch_2/options/{role}.txt"
			with open(filePath, "a") as support_options:
				support_options.write("\n" + heroName)
			return redirect('rosters')
	else:
		form = forms.Add_Hero_Form()
	return render(request, 'add_templates/Add_Hero.html', {'form': form})	

def Add_Map(request):
	if request.method == "POST":
		form = forms.Add_Map_Form(request.POST)
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
		form = forms.Add_Map_Form()
	return render(request, 'add_templates/Add_Map.html', {'form': form})

def Add_Sub_Map(request, mapName):
	if request.method == "POST":
		form = forms.Add_Control_Sub_Map_Form(request.POST)
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
		form = forms.Add_Control_Sub_Map_Form()
	return render(request, 'add_templates/Add_Sub_Map.html', {'form': form, 'mapName': mapName})

def Add_Match_Type(request):
	if request.method == "POST":
		form = forms.Add_Match_Type_Form(request.POST)
		if form.is_valid():
			matchType = form.cleaned_data["match_type"]
			with open("OverWatch_2\options\Match_Type.txt", "a") as match_options:
				match_options.write("\n" + matchType)
			return redirect('rosters')
	else:
		form = forms.Add_Match_Type_Form()
	return render(request, 'add_templates/Add_Match_Type.html', {'form': form})