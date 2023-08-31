from django.urls import path
from .views import Create_Team

urlpatterns = [
    path('create/', Create_Team, name='create-team'),
]
