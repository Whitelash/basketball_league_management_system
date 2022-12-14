from django.shortcuts import render
from django.views.generic import ( DetailView,
                                    ListView)
                                    
from .models import Level, Team, Player, Stats
from .models import *



# Create your views here.
class LevelListView(ListView):
    context_object_name = "levels"
    model = Level
    template_name = "league/level_list.html"

class TeamListView(DetailView):
    context_object_name = "teams"
    model = Team
    template_name ="league/team_list.html"

class PlayerListView(DetailView):
    context_object_name = 'players'
    model = Player
    template_name = "league/player_list"

class StatsListView(DetailView):
    context_object_name = 'stats'
    model = Stats
    template_name = "league/stats_list"