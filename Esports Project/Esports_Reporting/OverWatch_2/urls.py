from django.urls import path,include
from .views import team_views, add_views, data_views, match_views, delete_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Team Paths
	path('rosters/', team_views.ow_rosters, name='rosters'),
	path('team/<int:pk>/', team_views.ow_team_roster, name='team-roster'),
	path('team/<int:pk>/ActivePlayer/', team_views.activate_player, name='active-player'),
    
	# Add Paths
	path('createTeam/', add_views.create_ow_team, name='create-team'),
	path('team/<int:pk>/addPlayer/', add_views.add_player_to_roster, name='add-roster-player'),
	path('addHero/', add_views.add_hero, name='add-hero'),
	path('addMap/', add_views.add_map, name='add-map'),
	path('<int:pk>/addSubMap/', add_views.add_sub_map, name='add-sub-map'),
	path('addMatchType/', add_views.add_match_type, name='add-match-type'),
    
	# Delete Paths
	path('deleteMatchType/', delete_views.delete_match_type, name='delete-match-type'),
	path('team/<int:pk>/deleteRosterPlayer/', delete_views.delete_roster_player, name='delete-roster-player'),
	path('team/<int:pk>/deleteTeam/', delete_views.delete_team, name='delete-team'),
	path('team/<int:pk>/deleteMatch/', delete_views.delete_match, name='delete-match'),
	path('team/<int:pk>/deleteGame/', delete_views.delete_game, name='delete-game'),
	path('team/<str:mapType>/<int:pk>/deleteMap/', delete_views.delete_map, name='delete-map'),
	path('team/<int:pk>/deletePlayer/', delete_views.delete_player, name='delete-player'),
	path('deleteHero/', delete_views.delete_hero, name='delete-hero'),
	path('deleteMap/', delete_views.delete_map_name, name='delete-map-name'),
    
	# Match Paths
	path('team/<int:pk>/addMatch/', match_views.add_match, name='add-match'),
	path('match/<int:pk>/addGame/', match_views.add_game, name='add-game'),
	path('game/<int:pk>/addControl/',match_views.add_control, name='add-control'),
	path('game/<int:pk>/addEscortHybrid/', match_views.add_escort_hybrid, name='add-escort-hybrid'),
	path('game/<int:pk>/addPush/', match_views.add_push, name='add-push'),
	path('game/<int:pk>/addFlashpoint/', match_views.add_flashpoint, name='add-flashpoint'),
    path('game/<int:pk>/addClash/', match_views.add_clash, name='add-clash'),
	path('game/<str:mapType>/<int:pk>/addPlayer/', match_views.add_player, name='add-player'),
	path('game/<str:mapType>/<int:pk>/addSinglePlayer/', match_views.add_single_player, name='add-single-player'),
    
	# Data Paths
	path('player/<int:pk>/', data_views.player_data, name='player-data'),
    path('mapStats/<int:pk>/control', data_views.control_stats, name='control-stats'),
	path('mapStats/<int:pk>/escortHybrid/<str:map_type>', data_views.escort_hybrid_stats, name='escort-hybrid-stats'),
	path('mapStats/<int:pk>/clash', data_views.clash_stats, name='clash-stats'),
	path('mapStats/<int:pk>/flashpoint', data_views.flashpoint_stats, name='flashpoint-stats'),
	path('mapStats/<int:pk>/push', data_views.push_stats, name='push-stats'),
    
	# Logout Path
	path('logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

