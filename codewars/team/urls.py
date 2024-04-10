from django.urls import path
from .views import create_script , create_team , join_team , edit_script , view_scripts , view_stats , runscript
urlpatterns = [
    path('create_script/', create_script, name='create_script'),
    path('join_team/<int:pk>/', join_team, name='join_team'),
    path('create_team/<int:pk>/', create_team, name='create_team'),
    path('edit_script/', edit_script, name='edit_script'),
    path('view_scripts/', view_scripts, name='view_scripts'),
    path('view_stats/', view_stats, name='view_stats'),
    path('runscript/', runscript, name='runscript'),
]
