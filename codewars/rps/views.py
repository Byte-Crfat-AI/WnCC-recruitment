from .serializers import GameSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Team_stats
from .serializers import TeamSerializer_stats
def Game(team1_choice , team2_choice):
    winning_combinations = {
        'rock': {'scissors'},
        'paper': {'rock'},
        'scissors': {'paper'}
    }

    # Check if choices are valid
    if team1_choice not in winning_combinations or team2_choice not in winning_combinations:
        return "Invalid choices"

    # Determine the winner
    if team1_choice == team2_choice:
        return "It's a tie!"
    elif team2_choice in winning_combinations[team1_choice]:
        return "Team 1 wins!"
    else:
        return "Team 2 wins!"
@api_view(['POST'])
def play_game(request):
    team1_choice = request.data.get('team1_choice')
    team2_choice = request.data.get('team2_choice')
    if team1_choice==0:
        team1_choice = 'rock'
    elif team1_choice==1:    
        team1_choice = 'paper'      
    else:    
        team1_choice = 'scissors'
    if team2_choice==0:   
        team2_choice = 'rock'   
    elif team2_choice==1:
        team2_choice = 'paper'
    else:
        team2_choice = 'scissors'
    game = Game(team1_choice=team1_choice, team2_choice=team2_choice)
    if game == 'Team 1 wins!' :
        request.data['winner'] = request.data['team1']
    elif game == 'Team 2 wins!' :    
        request.data['winner'] = request.data['team2']  
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        game = serializer.save()
        try :
            ourteam = Team_stats.objects.get(name = game.team1)
            if(game.winner == game.team1):
                ourteam.wins += 1
            elif(game.winner == game.team2):
                ourteam.losses += 1
            else:
                ourteam.ties += 1
            ourteam.games_played += 1
            ourteam.win_percentage = (ourteam.wins/ourteam.games_played)*100
            ourteam.save()
        except Team_stats.DoesNotExist:
            pass
        w = 0
        l = 0
        t = 0
        wp = 0
        if game.winner == game.team1:
            w = 1
            wp = 100
        elif game.winner == game.team2:
            l = 1
            wp = 0
        else:
            t = 1
            wp = 50
        data = {
            'name':game.team1,
            'wins':w,
            'losses':l,
            'ties':t,
            'win_percentage':wp,
            'games_played':1,
            'code':game.team1.code
        }
        stat_serializer = TeamSerializer_stats(data=data)
        if stat_serializer.is_valid():
            stat_serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)