# Generated by Django 5.0.1 on 2024-04-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_choice', models.CharField(max_length=10)),
                ('player2_choice', models.CharField(max_length=10)),
                ('winner', models.CharField(max_length=10)),
            ],
        ),
    ]
