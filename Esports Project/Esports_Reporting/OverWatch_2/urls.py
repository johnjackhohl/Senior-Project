from django.urls import path,include
from .views import team_views, add_views, data_views, match_views, delete_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

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
	path('game/<str:mapType>/<int:pk>/addSinglePlayer/', match_views.Add_Single_Player, name='add-single-player'),
	path('addHero/', add_views.Add_Hero, name='add-hero'),
	path('addMap/', add_views.Add_Map, name='add-map'),
	path('<int:pk>/addSubMap/', add_views.Add_Sub_Map, name='add-sub-map'),
	path('deleteHero/', delete_views.Delete_Hero, name='delete-hero'),
	path('deleteMap/', delete_views.Delete_Map_Name, name='delete-map-name'),
	path('addMatchType/', add_views.Add_Match_Type, name='add-match-type'),
	path('deleteMatchType/', delete_views.Delete_Match_Type, name='delete-match-type'),
	path('team/<int:pk>/deleteRosterPlayer/', delete_views.Delete_Roster_Player, name='delete-roster-player'),
	path('team/<int:pk>/deleteTeam/', delete_views.Delete_Team, name='delete-team'),
	path('team/<int:pk>/deleteMatch/', delete_views.Delete_Match, name='delete-match'),
	path('team/<int:pk>/deleteGame/', delete_views.Delete_Game, name='delete-game'),
	path('team/<str:mapType>/<int:pk>/deleteMap/', delete_views.Delete_Map, name='delete-map'),
	path('team/<int:pk>/deletePlayer/', delete_views.Delete_Player, name='delete-player'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('team/<int:pk>/ActivePlayer/', team_views.Activate_Player, name='active-player'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

