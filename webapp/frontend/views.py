from django.shortcuts import render

def game_page(request):
    """View to render the chess game HTML page."""
    return render(request, 'frontend/game.html')