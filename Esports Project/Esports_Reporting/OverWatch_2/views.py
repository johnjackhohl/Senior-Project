from django.shortcuts import render, redirect
from .forms import OW_Team_Form, Roster_Form
from .models import OW_Team, Roster


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
        print(form)
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
