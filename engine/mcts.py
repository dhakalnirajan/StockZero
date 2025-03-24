import numpy as np
import chess
from django.core.cache import cache
from .model import PolicyValueNetwork # Ensure correct relative import
from .utils import move_to_index, index_to_move, board_to_input, get_legal_moves_mask, NUM_POSSIBLE_MOVES, get_game_result_value # Ensure correct relative import

class MCTSNode:
    def __init__(self, board, parent=None, prior_prob=0):
        self.board = board.copy()
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.value_sum = 0
        self.prior_prob = prior_prob
        self.policy_prob = 0
        self.value = 0

    def select_child(self, exploration_constant=1.4):
        best_child = None
        best_ucb = -float('inf')
        for move, child in self.children.items():
            ucb = child.value + exploration_constant * child.prior_prob * np.sqrt(self.visits) / (1 + child.visits)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child
        return best_child

    def expand(self, policy_probs):
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            move_index = move_to_index(move)
            prior_prob = policy_probs[move_index]
            self.children[move] = MCTSNode(chess.Board(fen=self.board.fen()), parent=self, prior_prob=prior_prob)

    def evaluate(self, policy_value_net):
        fen_str = self.board.fen()
        cached_evaluation = cache.get(fen_str) # Check cache first
        if cached_evaluation:
            policy_probs, value = cached_evaluation
            return value, policy_probs

        input_board = board_to_input(self.board)
        policy_output, value_output = policy_value_net(np.expand_dims(input_board, axis=0))
        policy_probs = policy_output.numpy()[0]
        value = value_output.numpy()[0][0]

        legal_moves_mask = get_legal_moves_mask(self.board)
        masked_policy_probs = policy_probs * legal_moves_mask
        if np.sum(masked_policy_probs) > 0:
            masked_policy_probs /= np.sum(masked_policy_probs)
        else:
            masked_policy_probs = legal_moves_mask / np.sum(legal_moves_mask)

        self.policy_prob = masked_policy_probs
        self.value = value

        cache.set(fen_str, (masked_policy_probs, value), timeout=300) # Cache for 5 minutes (adjust timeout)
        return value, masked_policy_probs

    def backup(self, value):
        self.visits += 1
        self.value_sum += value
        self.value = self.value_sum / self.visits
        if self.parent:
            self.parent.backup(-value)

def run_mcts(root_node, policy_value_net, num_simulations):
    for _ in range(num_simulations):
        node = root_node
        search_path = [node]

        while node.children and not node.board.is_game_over():
            node = node.select_child()
            search_path.append(node)

        leaf_node = search_path[-1]

        if not leaf_node.board.is_game_over():
            value, policy_probs = leaf_node.evaluate(policy_value_net)
            leaf_node.expand(policy_probs)
        else:
            value = get_game_result_value(leaf_node.board)

        leaf_node.backup(value)

    return choose_best_move_from_mcts(root_node)

def choose_best_move_from_mcts(root_node, temperature=0.0):
    if temperature == 0:
        best_move = max(root_node.children, key=lambda move: root_node.children[move].visits)
    else: # Not used in deployment, but kept for potential exploration
        visits = [root_node.children[move].visits for move in root_node.children]
        move_probs = np.array(visits) ** (1/temperature)
        move_probs = move_probs / np.sum(move_probs)
        moves = list(root_node.children.keys())
        best_move = np.random.choice(moves, p=move_probs)

    return best_move