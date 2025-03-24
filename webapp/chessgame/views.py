from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
import chess
import logging
from inference import get_optimized_ai_move
from engine.traditional_engine import call_AI as call_traditional_ai
from .serializers import MakeMoveRequestSerializer, MakeMoveResponseSerializer
from .models import GameRecord

logger = logging.getLogger('webapp') # Get webapp logger

@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle]) # Apply rate limiting
def make_move_api(request):
    """API endpoint to handle user moves and get optimized AI response, records game in PGN, production ready."""
    serializer = MakeMoveRequestSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Invalid make_move request data: {serializer.errors}") # Log invalid request data
        return Response(MakeMoveResponseSerializer({'error': serializer.errors}).data, status=status.HTTP_400_BAD_REQUEST)

    user_move_uci = serializer.validated_data['move']
    current_fen = serializer.validated_data['fen']

    board = chess.Board(fen=current_fen)
    game_pgn = chess.pgn.Game() # Initialize PGN game for this session
    game_pgn.headers["Event"] = "StockZero Chess Game"
    game_pgn.setup(board.fen())
    node = game_pgn.end() # Start PGN at current board position
    ai_player_color = "Black" if board.turn == chess.WHITE else "White" # Determine AI's color based on turn

    try:
        user_move = chess.Move.from_uci(user_move_uci)
        if user_move not in board.legal_moves:
            logger.warning(f"Illegal move attempted: {user_move_uci}, FEN: {current_fen}") # Log illegal move attempts
            return Response(MakeMoveResponseSerializer({'error': 'Illegal move'}).data, status=status.HTTP_400_BAD_REQUEST)

        node = node.add_variation(user_move, comment="User Move") # Add user move to PGN with comment
        board.push(user_move)

        if board.is_game_over():
            game_pgn.headers["Result"] = board.result() # Set game result in PGN
            game_pgn.headers["AI"] = f"StockZero Engine ({ai_player_color})" # Add AI engine info
            game_record = GameRecord.objects.create(
                pgn_content=game_pgn.export(as_str=True),
                result=board.result(),
                ai_player_color=ai_player_color,
                user=request.user if request.user.is_authenticated else None # Associate with user if authenticated
            )
            logger.info(f"Game over - Recorded PGN to database, Game ID: {game_record.id}, Result: {board.result()}") # Log game completion
            response_data = {'game_over': True, 'result': board.result(), 'next_fen': board.fen()}
            return Response(MakeMoveResponseSerializer(response_data).data)

        ai_move_uci = get_optimized_ai_move(board.fen(), num_simulations=100)
        ai_move = chess.Move.from_uci(ai_move_uci)

        node = node.add_variation(ai_move, comment="AI Move (StockZero)") # Add AI move to PGN with engine info
        board.push(ai_move)

        response_data = {'ai_move': ai_move_uci, 'next_fen': board.fen()}
        if board.is_game_over():
            game_pgn.headers["Result"] = board.result() # Set game result in PGN
            game_pgn.headers["AI"] = f"StockZero Engine ({ai_player_color})" # Add AI engine info
            game_record = GameRecord.objects.create(
                pgn_content=game_pgn.export(as_str=True),
                result=board.result(),
                ai_player_color=ai_player_color,
                user=request.user if request.user.is_authenticated else None # Associate with user if authenticated
            )
            logger.info(f"Game over - Recorded PGN to database, Game ID: {game_record.id}, Result: {board.result()}") # Log game completion
            response_data.update({'game_over': True, 'result': board.result()})

        return Response(MakeMoveResponseSerializer(response_data).data)

    except ValueError as ve:
        logger.error(f"ValueError processing move: {user_move_uci}, FEN: {current_fen}, Error: {ve}") # Log ValueErrors
        return Response(MakeMoveResponseSerializer({'error': 'Invalid move format'}).data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(f"Unexpected server error processing move: {user_move_uci}, FEN: {current_fen}") # Log unexpected errors with traceback
        return Response(MakeMoveResponseSerializer({'error': f'Server error: {str(e)}'}).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def make_traditional_move_api(request):
    """API endpoint to handle user moves and get move from the traditional engine."""
    serializer = MakeMoveRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(MakeMoveResponseSerializer({'error': serializer.errors}).data, status=status.HTTP_400_BAD_REQUEST)

    user_move_uci = serializer.validated_data['move']
    current_fen = serializer.validated_data['fen']

    board = chess.Board(fen=current_fen)
    game_pgn = chess.pgn.Game()
    game_pgn.headers["Event"] = "Traditional Chess Game"
    game_pgn.setup(board.fen())
    node = game_pgn.end()

    try:
        user_move = chess.Move.from_uci(user_move_uci)
        if user_move not in board.legal_moves:
            return Response(MakeMoveResponseSerializer({'error': 'Illegal move'}).data, status=status.HTTP_400_BAD_REQUEST)

        node = node.add_variation(user_move, comment="User Move")
        board.push(user_move)

        if board.is_game_over():
            game_pgn.headers["Result"] = board.result()
            GameRecord.objects.create(pgn_content=game_pgn.export(as_str=True), result=board.result(), ai_player_color="Traditional AI", user=request.user if request.user.is_authenticated else None)
            response_data = {'game_over': True, 'result': board.result(), 'next_fen': board.fen()}
            return Response(MakeMoveResponseSerializer(response_data).data)

        ai_move_uci = call_traditional_ai(board.fen(), level=2) # Call traditional engine, depth=2 (adjust depth)
        ai_move = chess.Move.from_uci(ai_move_uci)

        node = node.add_variation(ai_move, comment="Traditional AI Move")
        board.push(ai_move)

        response_data = {'ai_move': ai_move_uci, 'next_fen': board.fen()}
        if board.is_game_over():
            game_pgn.headers["Result"] = board.result()
            GameRecord.objects.create(pgn_content=game_pgn.export(as_str=True), result=board.result(), ai_player_color="Traditional AI", user=request.user if request.user.is_authenticated else None)
            response_data.update({'game_over': True, 'result': board.result()})

        return Response(MakeMoveResponseSerializer(response_data).data)

    except ValueError:
        return Response(MakeMoveResponseSerializer({'error': 'Invalid move format'}).data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(MakeMoveResponseSerializer({'error': f'Server error: {str(e)}'}).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)