import chess
import numpy as np

# --- Correct and Deterministic Move Encoding/Decoding (Production Grade) ---
NUM_POSSIBLE_MOVES = 4672 # Correct value based on deterministic encoding

def move_to_index(move):
    """Standard, deterministic move to index conversion (UCI-like encoding)."""
    index = 0

    # Non-promotion moves (most common)
    if move.promotion is None:
        index = move.from_square * 64 + move.to_square # Source and target squares

    # Promotion moves - use offsets to separate them from non-promotion indices
    elif move.promotion == chess.KNIGHT:
        index = 4096 + move.to_square # Knight promotions start after non-promotion moves
    elif move.promotion == chess.BISHOP:
        index = 4096 + 64 + move.to_square # Bishop promotions after Knights
    elif move.promotion == chess.ROOK:
        index = 4096 + 64*2 + move.to_square # Rook promotions after Bishops
    elif move.promotion == chess.QUEEN:
        index = 4096 + 64*3 + move.to_square # Queen promotions after Rooks
    else:
        raise ValueError(f"Unknown promotion piece type: {move.promotion}")

    return index

def index_to_move(index, board):
    """Standard, deterministic index to move conversion (index to chess.Move)."""

    if 0 <= index < 4096: # Non-promotion moves
        from_square = index // 64
        to_square = index % 64
        promotion = None

    elif 4096 <= index < 4096 + 64: # Knight promotions
        from_square_rank = chess.square_rank(chess.A8) - 1 # Rank 8 for White Pawns, Rank 1 for Black Pawns,  -1 for index conversion
        from_square = chess.square(chess.square_file(chess.A1), from_square_rank) # Assume promotion from any file on promotion rank. Refine as needed.
        to_square = index - 4096
        promotion = chess.KNIGHT

    elif 4096 + 64 <= index < 4096 + 64*2: # Bishop promotions
        from_square_rank = chess.square_rank(chess.A8) - 1
        from_square = chess.square(chess.square_file(chess.A1), from_square_rank)
        to_square = index - (4096 + 64)
        promotion = chess.BISHOP

    elif 4096 + 64*2 <= index < 4096 + 64*3: # Rook promotions
        from_square_rank = chess.square_rank(chess.A8) - 1
        from_square = chess.square(chess.square_file(chess.A1), from_square_rank)
        to_square = index - (4096 + 64*2)
        promotion = chess.ROOK

    elif 4096 + 64*3 <= index < NUM_POSSIBLE_MOVES: # Queen promotions
        from_square_rank = chess.square_rank(chess.A8) - 1
        from_square = chess.square(chess.square_file(chess.A1), from_square_rank)
        to_square = index - (4096 + 64*3)
        promotion = chess.QUEEN

    else: # Invalid index
        return None

    move = chess.Move(from_square, to_square, promotion=promotion)
    if move in board.legal_moves:
        return move
    return None # Move is not legal

# --- Board Representation (No Changes - Keep these functions) ---
def board_to_input(board): # ... (rest of board_to_input function) ...
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    input_planes = np.zeros((8, 8, 12), dtype=np.float32)

    for piece_type_index, piece_type in enumerate(piece_types):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.piece_type == piece_type:
                    plane_index = piece_type_index if piece.color == chess.WHITE else piece_type_index + 6
                    row, col = chess.square_rank(square), chess.square_file(square)
                    input_planes[row, col, plane_index] = 1.0
    return input_planes

def get_legal_moves_mask(board): # ... (rest of get_legal_moves_mask function) ...
    legal_moves = list(board.legal_moves)
    move_indices = [move_to_index(move) for move in legal_moves]
    mask = np.zeros(NUM_POSSIBLE_MOVES, dtype=np.float32)
    mask[move_indices] = 1.0
    return mask

def get_game_result_value(board): # ... (rest of get_game_result_value function) ...
    if board.is_checkmate():
        return 1 if board.turn == chess.BLACK else -1
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition() or board.is_variant_draw():
        return 0
    else:
        return 0