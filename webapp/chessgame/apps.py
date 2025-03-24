from django.apps import AppConfig

class ChessgameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp.chessgame'

    def ready(self):
        from engine import load_chess_engine
        load_chess_engine()