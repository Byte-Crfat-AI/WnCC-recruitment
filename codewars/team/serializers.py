from rest_framework import serializers
from .models import Team , Script 
import ast


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'member1' , 'member2' , 'member3' , 'lead' , 'code' ]
        
class ScriptSerializer(serializers.ModelSerializer):
    def validate_script(self, value):
        """
        Check if the provided script is a valid Python script.
        """
        try:
            ast.parse(value)
            return value
        except SyntaxError:
            raise serializers.ValidationError("Invalid Python script")
    class Meta:
        model = Script
        fields = ['script' , 'team']