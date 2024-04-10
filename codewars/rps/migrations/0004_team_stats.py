# Generated by Django 5.0.4 on 2024-04-09 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0003_game_team1_game_team2_alter_game_winner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team_stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('win_percentage', models.FloatField()),
                ('games_played', models.IntegerField()),
            ],
        ),
    ]