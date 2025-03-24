import chess
import tensorflow as tf
from engine import get_stockzero_engine, board_to_input, NUM_POSSIBLE_MOVES # Ensure correct relative import
from django.core.cache import cache # Django caching

def get_optimized_ai_move(board_fen, num_simulations=100, use_cache=True):
    """Optimized AI move inference function, using cache and GPU (if available)."""
    if use_cache:
        cached_move = cache.get(f"ai_move:{board_fen}")
        if cached_move:
            return cached_move

    engine = get_stockzero_engine() # Get pre-loaded engine
    board = chess.Board(fen=board_fen)

    # --- GPU Inference (TensorFlow should automatically use GPU if configured) ---
    with tf.device('/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'): # Explicitly place on GPU if available
        ai_move = engine.choose_move(board) # Engine's choose_move uses MCTS and NN inference

    ai_move_uci = ai_move.uci()

    if use_cache:
        cache.set(f"ai_move:{board_fen}", ai_move_uci, timeout=300) # Cache AI move for 5 minutes

    return ai_move_uci

if __name__ == "__main__":
    # Example usage (for testing inference)
    initial_fen = chess.STARTING_FEN
    ai_move = get_optimized_ai_move(initial_fen, num_simulations=100)
    print(f"AI move for starting position: {ai_move}")
    # Example: Measure inference time (for performance testing)
    import time
    start_time = time.time()
    ai_move_gpu = get_optimized_ai_move(initial_fen, num_simulations=200, use_cache=False) # No cache for time measurement
    end_time = time.time()
    inference_time = end_time - start_time
    print(f"AI move (no cache) on GPU: {ai_move_gpu}, Inference time: {inference_time:.4f} seconds")