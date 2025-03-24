import chess
import numpy as np
import time
import logging # Import logging
import os # Import os for file paths
from engine import get_stockzero_engine, get_game_result_value # Ensure correct relative import
from engine.utils import move_to_index, NUM_POSSIBLE_MOVES # Ensure correct relative import
from .data_utils import save_training_data # Import data saving utility

logger = logging.getLogger('training') # Get training logger

SELF_PLAY_DATA_DIR = os.path.join(os.path.dirname(__file__), 'self_play_data') # Directory for self-play data
os.makedirs(SELF_PLAY_DATA_DIR, exist_ok=True) # Create directory if it doesn't exist

def self_play_game(num_simulations, game_index):
    game_history = []
    board = chess.Board()
    engine = get_stockzero_engine() # Get trained engine instance
    game_pgn = chess.pgn.Game() # Initialize PGN game for self-play record
    game_pgn.headers["Event"] = "StockZero Self-Play Game"
    game_pgn.headers["Round"] = game_index + 1 # Game number in training run
    game_pgn.setup(board.fen())
    node = game_pgn.end()

    logger.info(f"Starting self-play game {game_index + 1}/{num_self_play_games}...")
    start_time = time.time()

    while not board.is_game_over():
        root_node = engine.rl_agent.MCTSNode(board) # Access MCTSNode via engine
        engine.rl_agent.run_mcts(root_node, engine.policy_value_net, num_simulations) # Run MCTS

        policy_targets = create_policy_targets_from_mcts_visits(root_node) # Function to create policy targets from visits
        game_history.append((board.fen(), policy_targets))

        best_move = engine.rl_agent.choose_best_move_from_mcts(root_node, temperature=0.8) # Exploration temp
        node = node.add_variation(best_move) # Add move to PGN tree
        board.push(best_move)

    game_result = get_game_result_value(board)
    game_pgn.headers["Result"] = board.result() # Set game result in PGN
    game_pgn.headers["Termination"] = board.outcome(claim_draw=True).termination.name # Add termination reason
    game_pgn.headers["PlyCount"] = board.ply() # Add ply count
    game_pgn.headers["AI-Engine"] = "StockZero" # Add engine info

    # Add game result to history as value targets
    for i in range(len(game_history)):
        fen, policy_target = game_history[i]
        game_history[i] = (fen, policy_target, game_result if board.turn == chess.WHITE else -game_result)

    end_time = time.time()
    game_time = end_time - start_time
    logger.info(f"Self-play game {game_index + 1}/{num_self_play_games} finished in {game_time:.2f} seconds, Result: {board.result()}, Termination: {board.outcome(claim_draw=True).termination.name}, PlyCount: {board.ply()}")

    # Save PGN to a file (optional, for analysis)
    pgn_filename = os.path.join(SELF_PLAY_DATA_DIR, f"self_play_game_{game_index + 1}.pgn")
    with open(pgn_filename, "w") as pgn_file:
        pgn_file.write(game_pgn.export(as_str=True))
    logger.info(f"PGN saved to: {pgn_filename}")

    return game_history

def create_policy_targets_from_mcts_visits(root_node):
    """Creates policy target vector from MCTS visit counts (moved from views to training utils)."""
    policy_targets = np.zeros(NUM_POSSIBLE_MOVES, dtype=np.float32)
    for move, child_node in root_node.children.items():
        move_index = move_to_index(move) # Access move_to_index via engine.utils
        policy_targets[move_index] = child_node.visits
    policy_targets /= np.sum(policy_targets)
    return policy_targets

if __name__ == "__main__":
    # Example usage (for testing self-play generation)
    num_self_play_games = 2 # Example number of games for testing
    all_game_histories = []
    for i in range(num_self_play_games):
        game_history = self_play_game(num_simulations=50, game_index=i)
        all_game_histories.append(game_history)

    # Example: Save game histories to files (using data_utils)
    save_training_data(all_game_histories, filename=os.path.join(SELF_PLAY_DATA_DIR, "example_self_play_games.pkl"))
    print(f"Generated {num_self_play_games} self-play games and saved example data.")