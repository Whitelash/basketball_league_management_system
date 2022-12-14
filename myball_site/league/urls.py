from django.urls import path
from . import views

app_name = 'league'
urlpatterns = [
    path('',views.LevelListView.as_view(), name='level_list'),
    path('<slug:slug>/', views.TeamListView.as_view(), name='team_list'),
    path('<str:league>/<slug:slug>/', views.PlayerListView.as_view(), name='player_list'),
    path('<str:league>/<slug:slug>/', views.StatsListView.as_view(), name='stats_list'),
]
