from django.urls import path
from . import views

urlpatterns = [
    path('make_move/', views.make_move_api, name='make_move_api'), # RL-based engine API
    path('make_traditional_move/', views.make_traditional_move_api, name='make_traditional_move_api'), # Traditional engine API
]