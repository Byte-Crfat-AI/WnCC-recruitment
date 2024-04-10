from django.db import models

class Game(models.Model):
    team1_choice = models.CharField(max_length=10)
    team2_choice = models.CharField(max_length=10)
    team1 = models.CharField(max_length=50 ,null=True)
    team2 = models.CharField(max_length=50 , null=True)
    winner = models.CharField(max_length=50)
# Create your models here.
class Team_stats(models.Model):
    name = models.CharField(max_length=50 , unique=True)
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    win_percentage = models.FloatField()
    games_played = models.IntegerField()
    def __str__(self):
        return self.name