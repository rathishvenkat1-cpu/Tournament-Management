from django.contrib import admin
from django.contrib import admin
from .models import Player, Tournament, Match


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "rating")
    search_fields = ("name", "country")


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "start_date", "end_date")
    filter_horizontal = ("players",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tournament",
        "player1",
        "player2",
        "winner",
        "round_number",
        "played_at",
    )
