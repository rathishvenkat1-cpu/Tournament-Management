from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    players = models.ManyToManyField(Player)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="matches"
    )

    player1 = models.ForeignKey(
        Player,
        related_name="player1_matches",
        on_delete=models.CASCADE
    )

    player2 = models.ForeignKey(
        Player,
        related_name="player2_matches",
        on_delete=models.CASCADE
    )

    winner = models.ForeignKey(
        Player,
        related_name="winner_matches",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    round_number = models.PositiveIntegerField(default=1)

    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["played_at"]

    def __str__(self):
        return f"{self.player1} vs {self.player2}"