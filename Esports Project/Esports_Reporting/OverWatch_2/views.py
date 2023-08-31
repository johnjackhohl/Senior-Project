from django.shortcuts import render, redirect
from .forms import OW_Team_Form

# Create your views here.
def Create_Team(request):
    if request.method == "POST":
        form = OW_Team_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Rosters')
    else:
        form = OW_Team_Form()
    return render(request, 'Create_Team.html', {'form': form})
