from django.urls import path
from . import views

urlpatterns = [

    # -------------------------
    # Home
    # -------------------------
     path("", views.home, name="home"),

    # -------------------------
    # Authentication
    # -------------------------
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # -------------------------
    # Dashboard
    # -------------------------
    path("dashboard/", views.dashboard, name="dashboard"),

    # -------------------------
    # Player URLs
    # -------------------------
    path("players/", views.player_list, name="player_list"),
    path("players/add/", views.player_add, name="player_add"),
    path("players/edit/<int:pk>/", views.player_edit, name="player_edit"),
    path("players/delete/<int:pk>/", views.player_delete, name="player_delete"),

    # -------------------------
    # Tournament URLs
    # -------------------------
    path("tournaments/", views.tournament_list, name="tournament_list"),
    path("tournaments/add/", views.tournament_add, name="tournament_add"),
    path("tournaments/edit/<int:pk>/", views.tournament_edit, name="tournament_edit"),
    path("tournaments/delete/<int:pk>/", views.tournament_delete, name="tournament_delete"),

    # -------------------------
    # Match URLs
    # -------------------------
    path(
        "tournament/<int:tournament_id>/generate/",
        views.generate_matches,
        name="generate_matches",
    ),

    path(
        "tournament/<int:tournament_id>/matches/",
        views.match_list,
        name="match_list",
    ),

    # -------------------------
    # Ranking URLs
    # -------------------------
    path(
        "tournament/<int:tournament_id>/ranking/",
        views.ranking,
        name="ranking",
    ),

    path(
        "ranking/pdf/<int:tournament_id>/",
        views.export_pdf,
        name="export_pdf",
    ),

    path(
        "ranking/excel/<int:tournament_id>/",
        views.export_excel,
        name="export_excel",
    ),
]