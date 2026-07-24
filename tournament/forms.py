from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player, Tournament, Match


# -------------------------
# User Registration Form
# -------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


# -------------------------
# Player Form
# -------------------------
class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = [
            "name",
            "age",
            "country",
            "rating",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]

        qs = Player.objects.filter(name__iexact=name)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "Player already exists."
            )

        return name


# -------------------------
# Tournament Form
# -------------------------
class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = [
            "name",
            "location",
            "start_date",
            "end_date",
            "players",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "players": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }

    def clean_players(self):
        players = self.cleaned_data["players"]

        if len(players) % 2 != 0:
            raise forms.ValidationError(
                "Number of players must be even."
            )

        if len(players) < 2:
            raise forms.ValidationError(
                "Select at least 2 players."
            )

        return players

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end < start:
            raise forms.ValidationError(
                "End date cannot be before start date."
            )

        return cleaned_data


# -------------------------
# Match Form
# -------------------------
class MatchForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = [
            "tournament",
            "player1",
            "player2",
            "winner",
            "round_number",
        ]

        widgets = {
            "tournament": forms.Select(attrs={"class": "form-control"}),
            "player1": forms.Select(attrs={"class": "form-control"}),
            "player2": forms.Select(attrs={"class": "form-control"}),
            "winner": forms.Select(attrs={"class": "form-control"}),
            "round_number": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        player1 = cleaned_data.get("player1")
        player2 = cleaned_data.get("player2")
        winner = cleaned_data.get("winner")

        if player1 and player2 and player1 == player2:
            raise forms.ValidationError(
                "Player 1 and Player 2 cannot be the same."
            )

        if winner and winner not in [player1, player2]:
            raise forms.ValidationError(
                "Winner must be one of the selected players."
            )

        return cleaned_data