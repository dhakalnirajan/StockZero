from .mcts import run_mcts, MCTSNode # Ensure correct relative import

class RLEngine:
    def __init__(self, policy_value_net, num_simulations_per_move=100):
        self.policy_value_net = policy_value_net
        self.num_simulations_per_move = num_simulations_per_move

    def choose_move(self, board):
        root_node = MCTSNode(board)
        best_move = run_mcts(root_node, self.policy_value_net, self.num_simulations_per_move)
        return best_move