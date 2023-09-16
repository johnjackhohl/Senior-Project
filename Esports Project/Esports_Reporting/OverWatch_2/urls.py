from django.urls import path
from .views import team_views, add_views, data_views, match_views, delete_views
urlpatterns = [
	path('createTeam/', add_views.Create_OW_Team, name='create-team'),
	path('rosters/', team_views.OW_Rosters, name='rosters'),
	path('team/<int:pk>/', team_views.OW_Team_Roster, name='team-roster'),
	path('team/<int:pk>/addPlayer/', add_views.Add_Player_to_Roster, name='add-roster-player'),
	path('team/<int:pk>/addMatch/', match_views.Add_Match, name='add-match'),
	path('match/<int:pk>/addGame/', match_views.Add_Game, name='add-game'),
	path('game/<int:pk>/addControl/',match_views.Add_Control, name='add-control'),
	path('game/<int:pk>/addEscortHybrid/', match_views.Add_Escort_Hybrid, name='add-escort-hybrid'),
	path('game/<int:pk>/addPush/', match_views.Add_Push, name='add-push'),
	path('game/<int:pk>/addFlashpoint/', match_views.Add_Flashpoint, name='add-flashpoint'),
	path('game/<str:mapType>/<int:pk>/addPlayer/', match_views.Add_Player, name='add-player'),
	path('addHero/', add_views.Add_Hero, name='add-hero'),
	path('addMap/', add_views.Add_Map, name='add-map'),
	path('<str:mapName>/addSubMap/', add_views.Add_Sub_Map, name='add-sub-map'),
	path('deleteHero/', delete_views.Delete_Hero, name='delete-hero'),
	path('deleteMap/', delete_views.Delete_Map, name='delete-map'),
	path('addMatchType/', add_views.Add_Match_Type, name='add-match-type'),
	path('deleteMatchType/', delete_views.Delete_Match_Type, name='delete-match-type'),
	path('team/<int:pk>/deleteRosterPlayer/', delete_views.Delete_Roster_Player, name='delete-roster-player'),
	path('team/<int:pk>/deleteTeam/', delete_views.delete_team_info, name='delete-team'),
]
