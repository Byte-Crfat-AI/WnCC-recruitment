from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from django.shortcuts import redirect
from django.urls import reverse
from .models import Team
from .serializers import TeamSerializer
from .models import Script
from .serializers import ScriptSerializer
from players.models import CustomUser as Player
from rps.models import Team_stats
from rps.serializers import TeamSerializer_stats
@api_view(['POST'])
def create_team(request , pk):
    if request.method == 'POST':
        try:
           player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return Response({"error": "Player does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the team already exists with the given code
            code = serializer.validated_data.get('code')
            if Team.objects.filter(code=code).exists():
                return Response({'error': 'Team code already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the team has less than four members
            if Team.objects.filter(code=code).count() >= 4:
                return Response({'error': 'Team already has four members'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the team
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def join_team(request , pk):
    if request.method == 'POST':
        try:
           player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return Response({"error": "Player does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        code = request.data.get('code')
        player_id = request.data.get('player_id')
        try:
            team = Team.objects.get(code=code)
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if Team.objects.filter(code=code).count() >= 4:
            return Response({'error': 'Team already has four members'}, status=status.HTTP_400_BAD_REQUEST)
        if team.member1.id == player_id or team.member2.id == player_id or team.member3.id == player_id:
            return Response({'error': 'Player is already a member of the team'}, status=status.HTTP_400_BAD_REQUEST)
        if team.member1 is None:
            team.member1_id = player_id
        elif team.member2 is None:
            team.member2_id = player_id
        elif team.member3 is None:
            team.member3_id = player_id
        else:
            return Response({'error': 'Team already has four members'}, status=status.HTTP_400_BAD_REQUEST)
        team.save()
        return Response({'message': 'Player joined the team successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_script(request):
    if request.method == 'POST':
        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the player belongs to a team
            player_id = serializer.validated_data.get('player_id')
            team_id = serializer.validated_data.get('team_id')
            # Check if the player belongs to the team
            if not Team.objects.filter(id=team_id, member1_id=player_id) and \
               not Team.objects.filter(id=team_id, member2_id=player_id) and \
               not Team.objects.filter(id=team_id, member3_id=player_id) and \
               not Team.objects.filter(id=team_id, member4_id=player_id):
                return Response({'error': 'Player does not belong to the team'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the script
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def view_scripts(request):
    if request.method == 'GET':
        try:
            scripts = Script.objects.filter(team_id=request.data.get('team_id'))
        except Script.DoesNotExist:
            return Response({'error': 'Scripts do not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScriptSerializer(scripts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT' , 'PATCH' , 'DELETE'])
def edit_script(request):
    try:
        script = Script.objects.get(id=request.data.get('script_id'))
    except Script.DoesNotExist:
        return Response({'error': 'Script does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = ScriptSerializer(script, data=request.data, partial=True)
        if serializer.is_valid():
            # Check if the player belongs to the team of the script
            player_id = serializer.validated_data.get('player_id')
            team_id = serializer.validated_data.get('team_id')
            # Check if the player belongs to the team
            if not Team.objects.filter(id=team_id, member1_id=player_id) and \
               not Team.objects.filter(id=team_id, member2_id=player_id) and \
               not Team.objects.filter(id=team_id, member3_id=player_id) and \
               not Team.objects.filter(id=team_id, member4_id=player_id):
                return Response({'error': 'Player does not belong to the team'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        script.delete()
        return Response({'message': 'Script deleted successfully'},status=status.HTTP_204_NO_CONTENT)
       
            
@api_view(['POST'])
def runscript(request):
    if request.method == 'POST':
        try:
            team = Team.objects.get(name=request.data.get('name'))
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try:
            script = Script.objects.get(name=team.name)
        except Script.DoesNotExist:
            return Response({'error': 'Script does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # Run the script
        try:
            opponent = Team.objects.get(name=request.data.get('opponent'))
        except Team.DoesNotExist:
            return Response({'error': 'opponent does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try:
            opp_script = Script.objects.get(name=opponent.name)
        except Script.DoesNotExist:
            return Response({'error': 'Opponent Script does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # Run the script
        # Create a dictionary to store the local variables after script execution
        locals_dict = {}
        exec(script.code, globals(), locals_dict)
        script_result = int(locals_dict.get('result'))
        locals_dict = {}
        exec(opp_script.code, globals(), locals_dict)
        opp_script_result = int(locals_dict.get('result'))
        data = QueryDict(mutable=True)
        data.update({
            'team1_choice': script_result,
            'team2_choice': opp_script_result,
            'team1': team.name,
            'team2': opponent.name,
        })
        return redirect(reverse('rps:play_game'), data=data)
        # Now you can use script_result and opp_script_result as needed
@api_view(['GET'])
def view_stats(request):
    if request.method == 'GET':
        try:
            team = Team.objects.get(name=request.data.get('name') )
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
        try:
            stat = Team_stats.objects.get(name=team.name)
        except Team_stats.DoesNotExist:
            return Response({'error': 'Team stats do not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer_stats(stat)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)