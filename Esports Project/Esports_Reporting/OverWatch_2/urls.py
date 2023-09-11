from django.urls import path
from .views import *
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
    path('addHero/', Add_Hero, name='add-hero'),
    path('addMap/', Add_Map, name='add-map'),
    path('<str:mapName>/addSubMap/', Add_Sub_Map, name='add-sub-map'),
    path('deleteHero/', Delete_Hero, name='delete-hero'),
    path('deleteMap/', Delete_Map, name='delete-map'),
    path('addMatchType/', Add_Match_Type, name='add-match-type'),
    path('deleteMatchType/', Delete_Match_Type, name='delete-match-type'),
    path('team/<int:pk>/deleteRosterPlayer/', Delete_Roster_Player, name='delete-roster-player'),
]
