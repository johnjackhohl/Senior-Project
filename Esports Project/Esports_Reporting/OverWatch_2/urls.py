from django.urls import path
from .views import Create_OW_Team, OW_Roster, OW_Roster_Players, Add_Player_to_Roster, Add_Match, Add_Game, Add_Control, Add_Escort_Hybrid, Add_Push, Add_Flashpoint, Add_Player

urlpatterns = [
    path('createTeam/', Create_OW_Team, name='create-team'),
    path('rosters/', OW_Roster, name='rosters'),
    path('team/<int:pk>/', OW_Roster_Players, name='roster-players'),
    path('team/<int:pk>/addPlayer/', Add_Player_to_Roster, name='add-player'),
    path('team/<int:pk>/addMatch/', Add_Match, name='add-match'),
    path('match/<int:pk>/addGame/', Add_Game, name='add-game'),
    path('game/<int:pk>/addControl/', Add_Control, name='add-control'),
    path('game/<int:pk>/addEscortHybrid/', Add_Escort_Hybrid, name='add-escort-hybrid'),
    path('game/<int:pk>/addPush/', Add_Push, name='add-push'),
    path('game/<int:pk>/addFlashpoint/', Add_Flashpoint, name='add-flashpoint'),
    path('game/<int:pk>/addPlayer/', Add_Player, name='add-player'),
]
