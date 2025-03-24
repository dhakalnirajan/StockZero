from django.db import models
from django.conf import settings # Import settings for user model

class GameRecord(models.Model):
    pgn_content = models.TextField(help_text="PGN format of the chess game")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the game record was created")
    result = models.CharField(max_length=10, blank=True, help_text="Result of the game (e.g., 1-0, 0-1, 1/2-1/2)") # Store result explicitly
    ai_player_color = models.CharField(max_length=10, blank=True, help_text="Color played by AI (White or Black)") # Store AI color
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, help_text="User who played the game (optional)") # Link to User model if user authentication is added

    def __str__(self):
        return f"Game recorded on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Game Record"
        verbose_name_plural = "Game Records"
        ordering = ['-timestamp'] # Order by most recent first