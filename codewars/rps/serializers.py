from rest_framework import serializers
from .models import Game, Team_stats
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['team1_choice', 'team2_choice', 'winner' , 'team1' , 'team2']
class TeamSerializer_stats(serializers.ModelSerializer):
    class Meta:
        model = Team_stats
        fields = ['name', 'wins', 'losses' , 'ties' , 'win_percentage' , 'games_played' ]

