from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
import random
from django.http import HttpResponse
from django.db.models import Count, Q
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Player, Tournament, Match
from .forms import (
    RegisterForm,
    PlayerForm,
    TournamentForm,
    MatchForm,
)


# =====================================
# Home Page
# =====================================
def home(request):
    return render(request, "home.html")


# =====================================
# Register
# =====================================
def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Registration successful."
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )


# =====================================
# Login
# =====================================
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:

            login(request, user)

            messages.success(
                request,
                "Login Successful."
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

    return render(
        request,
        "registration/login.html"
    )


# =====================================
# Logout
# =====================================
@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


# =====================================
# Dashboard
# =====================================
@login_required
def dashboard(request):

    player_count = Player.objects.count()

    tournament_count = Tournament.objects.count()

    match_count = Match.objects.count()

    context = {

        "player_count": Player.objects.count(),

         "tournament_count": Tournament.objects.count(),

         "match_count": Match.objects.count(),

         "completed_matches": Match.objects.exclude(
           winner=None
         ).count(),

    }

    return render(
        request,
        "dashboard.html",
        context,
    )
    
# =====================================
# PLAYER LIST
# =====================================
@login_required
def player_list(request):

    search = request.GET.get("search", "")

    players = Player.objects.all()

    if search:
        players = players.filter(name__icontains=search)

    paginator = Paginator(players, 5)   # 5 players per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(
        request,
        "players/player_list.html",
        context,
    )


# =====================================
# ADD PLAYER
# =====================================
@login_required
def player_add(request):

    if request.method == "POST":

        form = PlayerForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Player added successfully."
            )

            return redirect("player_list")

    else:

        form = PlayerForm()

    return render(
        request,
        "players/player_form.html",
        {
            "form": form,
            "title": "Add Player",
        },
    )


# =====================================
# EDIT PLAYER
# =====================================
@login_required
def player_edit(request, pk):

    player = get_object_or_404(Player, pk=pk)

    if request.method == "POST":

        form = PlayerForm(
            request.POST,
            instance=player,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Player updated successfully."
            )

            return redirect("player_list")

    else:

        form = PlayerForm(instance=player)

    return render(
        request,
        "players/player_form.html",
        {
            "form": form,
            "title": "Edit Player",
        },
    )


# =====================================
# DELETE PLAYER
# =====================================
@login_required
def player_delete(request, pk):

    player = get_object_or_404(
        Player,
        pk=pk,
    )

    if request.method == "POST":

        player.delete()

        messages.success(
            request,
            "Player deleted successfully."
        )

        return redirect("player_list")

    return render(
        request,
        "players/player_delete.html",
        {
            "player": player,
        },
    )
# =====================================
# TORNAMENT_LIST
# =====================================

@login_required
def tournament_list(request):

    search = request.GET.get("search", "")

    tournaments = Tournament.objects.all()

    if search:
        tournaments = tournaments.filter(name__icontains=search)

    paginator = Paginator(tournaments, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(
        request,
        "tournaments/tournament_list.html",
        context,
    )
# =====================================
# TORNAMENT_ADD
# =====================================

@login_required
def tournament_add(request):

    if request.method == "POST":

        form = TournamentForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Tournament created successfully."
            )

            return redirect("tournament_list")

    else:

        form = TournamentForm()

    return render(
        request,
        "tournaments/tournament_form.html",
        {
            "form": form,
            "title": "Add Tournament",
        },
    )
# =====================================
# TORNAMENT_EDIT
# =====================================

@login_required
def tournament_edit(request, pk):

    tournament = get_object_or_404(
        Tournament,
        pk=pk,
    )

    if request.method == "POST":

        form = TournamentForm(
            request.POST,
            instance=tournament,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Tournament updated successfully."
            )

            return redirect("tournament_list")

    else:

        form = TournamentForm(
            instance=tournament
        )

    return render(
        request,
        "tournaments/tournament_form.html",
        {
            "form": form,
            "title": "Edit Tournament",
        },
    )
# =====================================
# TORNAMENT_DELETE
# =====================================
@login_required
def tournament_delete(request, pk):

    tournament = get_object_or_404(
        Tournament,
        pk=pk,
    )

    if request.method == "POST":

        tournament.delete()

        messages.success(
            request,
            "Tournament deleted successfully."
        )

        return redirect("tournament_list")

    return render(
        request,
        "tournaments/tournament_delete.html",
        {
            "tournament": tournament,
        },
    )
# =====================================
# GENERATE_MATCHES
# =====================================
import random

@login_required
def generate_matches(request, tournament_id):

    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    players = list(tournament.players.all())

    if len(players) not in [4, 8]:
        messages.error(
            request,
            "Tournament must contain exactly 4 or 8 players."
        )
        return redirect("tournament_list")

    Match.objects.filter(
        tournament=tournament
    ).delete()

    random.shuffle(players)

    winners = []

    # ---------- ROUND 1 ----------
    round_no = 1

    for i in range(0, len(players), 2):

        player1 = players[i]
        player2 = players[i + 1]

        winner = random.choice([player1, player2])

        Match.objects.create(
            tournament=tournament,
            player1=player1,
            player2=player2,
            winner=winner,
            round_number=round_no
        )

        winners.append(winner)

    # ---------- ROUND 2 ----------
    round_no = 2

    finalists = []

    for i in range(0, len(winners), 2):

        player1 = winners[i]
        player2 = winners[i + 1]

        winner = random.choice([player1, player2])

        Match.objects.create(
            tournament=tournament,
            player1=player1,
            player2=player2,
            winner=winner,
            round_number=round_no
        )

        finalists.append(winner)

    # ---------- FINAL ----------
    if len(finalists) == 2:

        champion = random.choice(finalists)

        runner = finalists[0] if champion == finalists[1] else finalists[1]

        Match.objects.create(
            tournament=tournament,
            player1=champion,
            player2=runner,
            winner=champion,
            round_number=3
        )

    messages.success(
        request,
        "Tournament Generated Successfully."
    )

    return redirect(
        "match_list",
        tournament.id
    )

# =====================================
# MATCHE_LIST
# =====================================
@login_required
def match_list(request, tournament_id):

    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
    )

    matches = Match.objects.filter(
        tournament=tournament
    )

    return render(
        request,
        "matches/match_list.html",
        {
            "tournament": tournament,
            "matches": matches,
        },
    )

# =====================================
# RANKING
# =====================================
@login_required
def ranking(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    rankings = []

    for player in tournament.players.all():

        wins = Match.objects.filter(
            tournament=tournament,
            winner=player
        ).count()

        rankings.append({
            "player": player,
            "wins": wins,
        })

    rankings.sort(key=lambda x: x["wins"], reverse=True)

    return render(
        request,
        "rankings/ranking.html",
        {
            "tournament": tournament,
            "rankings": rankings,
        },
    )

# =====================================
# EXPORT_EXCEL
# =====================================
@login_required
def export_excel(request, tournament_id):

    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    rankings = (
        Match.objects
        .filter(tournament=tournament)
        .values("winner__name")
        .annotate(
            wins=Count("winner")
        )
        .order_by("-wins")
    )

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Rankings"

    sheet.append([
        "Rank",
        "Player",
        "Wins"
    ])

    rank = 1

    for row in rankings:

        sheet.append([
            rank,
            row["winner__name"],
            row["wins"]
        ])

        rank += 1

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="rankings.xlsx"'

    workbook.save(response)

    return response

# =====================================
# EXPORT_PDF
# =====================================
@login_required
def export_pdf(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    rankings = (
        Match.objects
        .filter(tournament=tournament)
        .values("winner__name")
        .annotate(
            wins=Count("winner")
        )
        .order_by("-wins")
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="ranking.pdf"'

    pdf = SimpleDocTemplate(response)

    data = [
        ["Rank", "Player", "Wins"]
    ]

    rank = 1

    for row in rankings:

        data.append([
            rank,
            row["winner__name"],
            row["wins"]
        ])

        rank += 1

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0,1), (-1,-1), colors.beige),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("BOTTOMPADDING", (0,0), (-1,0), 10),
        ])
    )

    pdf.build([table])

    return response