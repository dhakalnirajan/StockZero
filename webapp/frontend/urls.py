from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_page, name='game_page'), # Game page at root URL
]