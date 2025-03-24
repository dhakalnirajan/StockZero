import os # Import os module
from .model import PolicyValueNetwork
from .rl_agent import RLEngine
from .utils import NUM_POSSIBLE_MOVES

trained_engine = None
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models') # models/ dir in project root
MODEL_WEIGHTS_FILE = os.path.join(MODEL_DIR, "rl_chess_model.weights.h5") # Default model weights file path

def load_chess_engine():
    global trained_engine
    if trained_engine is None:
        policy_value_net = PolicyValueNetwork(NUM_POSSIBLE_MOVES)
        # Check if model weights file exists, if not, you might want to handle this case (e.g., raise exception, log warning)
        if not os.path.exists(MODEL_WEIGHTS_FILE):
            raise FileNotFoundError(f"Model weights file not found at: {MODEL_WEIGHTS_FILE}. Please train the model first and ensure the model weights file is placed in the models/ directory.")
        policy_value_net.load_weights(MODEL_WEIGHTS_FILE) # Load from models/ directory
        trained_engine = RLEngine(policy_value_net, num_simulations_per_move=100)

def get_ai_move(board_fen):
    global trained_engine
    if trained_engine is None:
        load_chess_engine()
    board = chess.Board(fen=board_fen)
    ai_move = trained_engine.choose_move(board)
    return ai_move.uci()

def get_stockzero_engine(): # Export function to get engine instance
    global trained_engine
    if trained_engine is None:
        load_chess_engine()
    return trained_engine