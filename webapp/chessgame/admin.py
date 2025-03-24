from django.contrib import admin
from .models import GameRecord

@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'result', 'ai_player_color', 'user') # Display more relevant fields in list view
    list_filter = ('timestamp', 'ai_player_color', 'result') # Add filters for easier searching
    search_fields = ('pgn_content', 'result', 'user__username', 'user__email') # Searchable fields
    readonly_fields = ('timestamp', 'pgn_content') # Make PGN content and timestamp read-only in admin

    fieldsets = ( # Organize fields in admin edit form
        ('Game Information', {
            'fields': ('timestamp', 'result', 'ai_player_color', 'user')
        }),
        ('PGN Content', {
            'fields': ('pgn_content',),
            'classes': ('collapse',), # Collapse PGN content by default for cleaner view
        }),
    )