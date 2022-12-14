from django.contrib import admin
from league.models import Level, Team, Player,Stats

# Register your models here.
admin.site.register(Level)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Stats)