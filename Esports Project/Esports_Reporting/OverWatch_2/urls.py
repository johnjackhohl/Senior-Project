from django.urls import path
from .views import Create_OW_Team, OW_Roster, OW_Roster_Players, Add_Player_to_Roster

urlpatterns = [
    path('createTeam/', Create_OW_Team, name='create-team'),
    path('rosters/', OW_Roster, name='rosters'),
    path('team/<int:pk>/', OW_Roster_Players, name='roster-players'),
    path('team/<int:pk>/addPlayer/', Add_Player_to_Roster, name='add-player')
]
