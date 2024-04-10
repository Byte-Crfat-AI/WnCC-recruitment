from django.db import models
from players.models import CustomUser as Player
# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50  , unique=True)
    code = models.CharField(max_length=10 , unique=True)
    member1 = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='team_member1')
    member2 = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='team_member2')
    member3 = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='team_member3')
    lead = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='lead')

    def __str__(self):
        return self.name
class Script(models.Model):
    script = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    def __str__(self):
        return self.script