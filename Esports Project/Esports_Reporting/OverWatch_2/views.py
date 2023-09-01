from django.shortcuts import render, redirect
from datetime import datetime
from .forms import OW_Team_Form, Roster_Form, Match_Form, Game_Form, Control_Map_Form
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
			form.save()
			if(match.match_type == "Control"):
				return redirect('add-control', pk=pk)
	else:
		form = Game_Form()
	return render(request, 'Add_Game.html', {'form': form, 'match': match})

def Add_Control(request, pk):
	game = Game.objects.get(id=pk)
	with open("Esports Project\Esports_Reporting\OverWatch_2\options\Tank.txt", "r") as tank_options:
		tanks = [line.strip() for line in tank_options]
	if request.method == "POST":
		form = Control_Map_Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('add-control', pk=pk)
	else:
		form = Control_Map_Form()
	return render(request, 'Add_Control.html', {'form': form, 'game': game, 'tanks': tanks})

