import tensorflow as tf
import numpy as np
import time
import logging # Import logging
import os # Import os for file paths
from engine import get_stockzero_engine, board_to_input, NUM_POSSIBLE_MOVES # Ensure correct relative import
from .data_utils import load_training_data, save_training_data # Ensure correct relative import

logger = logging.getLogger('training') # Get training logger

TRAINING_DATA_DIR = os.path.join(os.path.dirname(__file__), 'training_data') # Directory for training data
os.makedirs(TRAINING_DATA_DIR, exist_ok=True) # Create directory if it doesn't exist
CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), 'checkpoints') # Directory for checkpoints
os.makedirs(CHECKPOINT_DIR, exist_ok=True) # Create directory if it doesn't exist

def train_step(model, board_inputs, policy_targets, value_targets, optimizer):
    with tf.GradientTape() as tape:
        policy_outputs, value_outputs = model(board_inputs)
        policy_loss = tf.keras.losses.CategoricalCrossentropy()(policy_targets, policy_outputs)
        value_loss = tf.keras.losses.MeanSquaredError()(value_targets, value_outputs)
        total_loss = policy_loss + value_loss
    gradients = tape.gradient(total_loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return total_loss, policy_loss, value_loss

def train_network(model, game_histories, optimizer, epochs=10, batch_size=32, checkpoint_path=None, checkpoint_freq=5):
    all_board_inputs = []
    all_policy_targets = []
    all_value_targets = []

    for game_history in game_histories:
        for fen, policy_target, game_result in game_history:
            board = chess.Board(fen)
            all_board_inputs.append(board_to_input(board))
            all_policy_targets.append(policy_target)
            all_value_targets.append(np.array([game_result]))

    all_board_inputs = np.array(all_board_inputs)
    all_policy_targets = np.array(all_policy_targets)
    all_value_targets = np.array(all_value_targets)

    dataset = tf.data.Dataset.from_tensor_slices((all_board_inputs, all_policy_targets, all_value_targets))
    dataset = dataset.shuffle(buffer_size=len(all_board_inputs)).batch(batch_size).prefetch(tf.data.AUTOTUNE)

    for epoch in range(epochs):
        logger.info(f"Epoch {epoch+1}/{epochs} started...")
        epoch_start_time = time.time()
        epoch_losses = []
        for batch_inputs, batch_policy_targets, batch_value_targets in dataset:
            loss, p_loss, v_loss = train_step(model, batch_inputs, batch_policy_targets, batch_value_targets, optimizer)
            epoch_losses.append(loss.numpy())
            logger.debug(f"  Batch Loss: {loss:.4f}, Policy Loss: {p_loss:.4f}, Value Loss: {v_loss:.4f}") # Debug level batch loss

        avg_epoch_loss = np.mean(epoch_losses)
        logger.info(f"Epoch {epoch+1}/{epochs} completed in {time.time() - epoch_start_time:.2f} seconds, Avg. Loss: {avg_epoch_loss:.4f}")

        if checkpoint_path and (epoch + 1) % checkpoint_freq == 0: # Save checkpoint every checkpoint_freq epochs
            checkpoint_file = os.path.join(checkpoint_path, f"model_checkpoint_epoch_{epoch+1}.weights.h5")
            model.save_weights(checkpoint_file)
            logger.info(f"Model checkpoint saved at: {checkpoint_file}")

if __name__ == "__main__":
    # --- Training Script Execution ---
    from engine.model import PolicyValueNetwork # Correct relative import
    policy_value_net = PolicyValueNetwork(NUM_POSSIBLE_MOVES)
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    # --- Load game histories from file (for example) ---
    training_data_file = os.path.join(TRAINING_DATA_DIR, "self_play_games_training_data.pkl") # Example data file
    game_histories = load_training_data(training_data_file) # Load from data_utils

    if not game_histories:
        logger.warning(f"No training data loaded from {training_data_file}. Training will be skipped.")
    else:
        logger.info(f"Loaded {len(game_histories)} game histories for training.")
        start_time = time.time()
        train_network(policy_value_net, game_histories, optimizer, epochs=10, batch_size=32, checkpoint_path=CHECKPOINT_DIR, checkpoint_freq=2) # Example checkpointing
        end_time = time.time()
        training_time = end_time - start_time
        logger.info(f"Training completed in {training_time:.2f} seconds.")

        # --- Save the trained model weights (versioned filename) ---
        import datetime
        current_datetime = datetime.datetime.now()
        model_version_str = current_datetime.strftime("%Y-%m-%d")
        model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models') # models/ dir in project root
        os.makedirs(model_dir, exist_ok=True) # Create models/ directory if it doesn't exist
        model_save_path = os.path.join(model_dir, f"stockzero_model_v{model_version_str}.weights.h5") # Versioned filename in models/
        policy_value_net.save_weights(model_save_path)
        logger.info(f"Trained model weights saved to '{model_save_path}'")
        logger.info("Training finished.")