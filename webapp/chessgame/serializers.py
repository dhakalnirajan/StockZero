from rest_framework import serializers

class MakeMoveRequestSerializer(serializers.Serializer):
    move = serializers.CharField()
    fen = serializers.CharField()

class MakeMoveResponseSerializer(serializers.Serializer):
    ai_move = serializers.CharField(required=False, allow_null=True)
    next_fen = serializers.CharField()
    game_over = serializers.BooleanField()
    result = serializers.CharField(required=False, allow_null=True)
    error = serializers.CharField(required=False, allow_null=True)