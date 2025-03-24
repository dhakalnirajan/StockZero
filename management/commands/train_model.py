from django.core.management.base import BaseCommand, CommandError
import tensorflow as tf
import time
import datetime
from engine import get_stockzero_engine, board_to_input, NUM_POSSIBLE_MOVES # Ensure correct relative import
from training import self_play, train_network # Ensure correct relative import

class Command(BaseCommand):
    help = 'Trains the StockZero chess engine model'

    def add_arguments(self, parser):
        parser.add_argument('--games', type=int, default=20, help='Number of self-play games to generate per iteration.')
        parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs per iteration.')
        parser.add_argument('--simulations', type=int, default=50, help='Number of MCTS simulations per move in self-play.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting StockZero model training..."))

        # --- GPU Check ---
        if tf.config.list_physical_devices('GPU'):
            self.stdout.write(self.style.SUCCESS("GPU is available and will be used for training."))
            gpu_device = '/GPU:0'
        else:
            self.stdout.write(self.style.WARNING("GPU is not available. Training will use CPU (may be slow)."))
            gpu_device = '/CPU:0'

        with tf.device(gpu_device):
            policy_value_net = engine.model.PolicyValueNetwork(NUM_POSSIBLE_MOVES) # Correct relative import
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
            engine = get_stockzero_engine() # Get engine instance

            num_self_play_games = options['games']
            epochs = options['epochs']
            num_simulations = options['simulations']

            game_histories = []
            start_time = time.time()
            for i in range(num_self_play_games):
                self.stdout.write(f"Generating self-play game {i+1}/{num_self_play_games}...")
                game_history = self_play.self_play_game(num_simulations=num_simulations)
                game_histories.append(game_history)

            self.stdout.write("Starting network training...")
            train_network.train_network(policy_value_net, game_histories, optimizer, epochs=epochs)

            end_time = time.time()
            training_time = end_time - start_time
            self.stdout.write(self.style.SUCCESS(f"Training completed in {training_time:.2f} seconds."))

            # --- Versioned Model Saving ---
            current_datetime = datetime.datetime.now()
            model_version_str = current_datetime.strftime("%Y-%m-%d")
            model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models') # models/ dir in project root
            os.makedirs(model_dir, exist_ok=True) # Create models/ directory if it doesn't exist
            model_save_path = os.path.join(model_dir, f"stockzero_model_v{model_version_str}.weights.h5") # Versioned filename in models/
            policy_value_net.save_weights(model_save_path)
            self.stdout.write(self.style.SUCCESS(f"Trained model weights saved to '{model_save_path}' in models/ directory"))
            self.stdout.write(self.style.SUCCESS("StockZero model training finished."))