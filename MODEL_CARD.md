# StockZero: A Self-Play Reinforcement Learning Chess Engine

[![License](https://img.shields.io/static/v1?label=License&message=Apache&color=yellow&style=for-the-badge&)](https://github.com/dhakalnirajan/StockZero/blob/main/LICENSE)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF3F06?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
[![Huggingface](https://img.shields.io/badge/Hugging%20Face-FF3F06?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/nirajandhakal/StockZero-v2)

This model card describes **StockZero**, a self-play reinforcement learning chess engine trained using TensorFlow/Keras. It combines a policy-value neural network with Monte Carlo Tree Search (MCTS) for decision making. StockZero serves as an educational example of applying deep RL to the game of chess. This model card also includes information about the model's converted formats and their usage.

## Model Details

### Model Description

StockZero learns to play chess by playing against itself. The core component is a neural network that takes a chess board state as input and outputs:

1. **Policy**: A probability distribution over all legal moves, indicating which move the model thinks is best.
2. **Value**: An estimation of the win/loss probability from the current player's perspective.

The model is trained using self-play data generated through MCTS, which guides the engine to explore promising game states.

This model card is for StockZero version 2 (v2) model. While the v1 model has same architecture, it had less self-play to learn policy. V1 model was played on only 20 self-play policy training for testing purposes to see whether the model will converge to lower value while v2 was played on 50 self-play games during policy training on Google Colaboratory Free Tier Notebook because larger self-play would result in high compute demand which is what I currently can't afford.

**Note**: StockZero v3 will be trained and open sourced soon.

### Input

The model takes a chess board as input, represented as a 8x8x12 NumPy array. Each of the 12 channels in the input represent a specific piece type (Pawn, Knight, Bishop, Rook, Queen, King) for both white and black players, where each layer contains binary values.

### Output

The model outputs two vectors:

1. **Policy**: A probability distribution over `NUM_POSSIBLE_MOVES=4672` representing the probability of making each move, obtained using `softmax` activation.
2. **Value**: A single scalar value indicating win/loss probability from current player’s perspective, ranging from -1 (loss) to 1 (win), obtained using `tanh` activation.

### Model Architecture

The neural network architecture consists of:

* One Convolutional Layer: `Conv2D(32, 3, activation='relu', padding='same')`
* Flatten Layer: `Flatten()`
* Two Dense Layers:
  * `Dense(NUM_POSSIBLE_MOVES, activation='softmax', name='policy_head')` for move probabilities
  * `Dense(1, activation='tanh', name='value_head')` for win/loss estimation

### Training Data

The model was trained on data generated from self-play, playing chess games against itself, with the generated self-play games then used to train the network iteratively. This process is similar to the AlphaZero approach.

### Training Procedure

1. **Self-Play**: The engine plays against itself using MCTS to make move decisions, generating game trajectories.
2. **Data Collection**: During the self-play, the board state and MCTS visit counts are recorded as the target policy. The final game results are saved as the target value.
3. **Training**: The model learns from the self-play data using a combination of categorical cross-entropy for the policy and mean squared error for the value.

The optimizer used during training is **Adam** with a learning rate of 0.001.

### Training parameters

* `num_self_play_games = 50`
* `epochs = 5`
* `num_simulations_per_move=100`

### Model Versions

This model has been converted into several formats for flexible deployment:

* **TensorFlow SavedModel**:  A directory containing model architecture and weights, allowing for native tensorflow usage.
* **Keras Model (.keras)**: A full Keras model with architecture and weights, suitable for Keras environment.
* **Keras Weights (.h5)**: Only model weights that can be loaded to an existing `PolicyValueNetwork` in Keras/TensorFlow
* **PyTorch Model (.pth)**: Full PyTorch Model equivalent (architecture and weights).
* **PyTorch Weights (.pth)**: Model weights that can be loaded to `PyTorchPolicyValueNetwork`.
* **ONNX (.onnx)**: A standard format for interoperability with various machine learning frameworks.
* **TensorFlow Lite (.tflite)**: An efficient model format for mobile and embedded devices.
* **Raw Binary (.bin)**: Raw byte representation of all model weights, for use in custom implementations.
* **NumPy Array (.npz)**: Model weights saved as individual numpy arrays, which can be easily loaded in many environments.

The model files are versioned based on the training time to maintain uniqueness, as model names are added to the filename.
For example : `StockZero-2025-03-24-1727.weights.h5` or `converted_models-202503241727.zip`.

### Intended Use

The model is intended for research, experimentation, and education purposes. Potential applications include:

* Studying reinforcement learning algorithms applied to complex games.
* Developing chess playing AI.
* Serving as a base model for fine-tuning and further research.
* Deploying as a lightweight engine on constrained hardware (TFLite).
* Using in non-TensorFlow environments (PyTorch, ONNX).

### Limitations

* The model is not intended to compete against top-level chess engines.
* The training data is limited to a small number of self-play games (50 games), therefore the strength of the engine is limited.
* The model is trained on a single GPU, so longer training may require multi GPU support or longer runtime.

## Model Evaluation

### Loss Curve

The following image shows the training loss curve for the model:

![Training Loss Curve](https://huggingface.co/nirajandhakal/StockZero/resolve/main/StockZero-v2%20model%20evaluation.png)

This model was evaluated against a simple random move opponent using the `evaluate_model` method in the provided `evaluation_script.py`. The results are as follows:

* **Number of Games:** 200 (The model plays as both white and black in each game against the random agent.)
* **Win Rate:** 0.0150 (1.5%)
* **Draw Rate:** 0.6850 (68.5%)
* **Loss Rate:** 0.3000 (30%)

These scores indicate that the model, in its current state, is not a strong chess player. It draws a majority of games against a random opponent, but also loses a significant number. Further training and architecture improvements are needed to enhance its performance.

## Demo Game Video

You can see a demo game here:

[![StockZero Demo Gameplay Video](https://huggingface.co/nirajandhakal/StockZero-v2/resolve/main/demo_video_thumbnail.png)](https://huggingface.co/nirajandhakal/StockZero-v2/blob/main/v2-gameplay-svg-high-quality.mp4)

## How to Use

### Training

1. Upload `training_code.py` to Google Colab.
2. Run the script to train the model on Google Colab.
3. Download the zip file of the trained weights and model, that is provided automatically after the training is complete.

### Model Conversion

1. Place `conversion_script.py` in Google Colab, and make sure the saved weights are in the correct location.
2. Run the script to create model files of different formats inside a folder `converted_models`.
3. Download the zip file containing all converted models using the automatic Colab download, which is triggered at the end of the script.

### Inference

To use the model for inference, load the model weights into an instance of `PolicyValueNetwork` (or its PyTorch equivalent) and use the `board_to_input` and `get_legal_moves_mask` functions to prepare the input. The following code shows how to make predictions:

```python
import chess
import numpy as np
import tensorflow as tf

class PolicyValueNetwork(tf.keras.Model):
    def __init__(self, num_moves):
        super(PolicyValueNetwork, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')
        self.flatten = tf.keras.layers.Flatten()
        self.dense_policy = tf.keras.layers.Dense(num_moves, activation='softmax', name='policy_head')
        self.dense_value = tf.keras.layers.Dense(1, activation='tanh', name='value_head')

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.flatten(x)
        policy = self.dense_policy(x)
        value = self.dense_value(x)
        return policy, value

NUM_POSSIBLE_MOVES = 4672
NUM_INPUT_PLANES = 12

def board_to_input(board):
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    input_planes = np.zeros((8, 8, NUM_INPUT_PLANES), dtype=np.float32)
    for piece_type_index, piece_type in enumerate(piece_types):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.piece_type == piece_type:
                    plane_index = piece_type_index if piece.color == chess.WHITE else piece_type_index + 6
                    row, col = chess.square_rank(square), chess.square_file(square)
                    input_planes[row, col, plane_index] = 1.0
    return input_planes

def get_legal_moves_mask(board):
    legal_moves = list(board.legal_moves)
    move_indices = [move_to_index(move) for move in legal_moves]
    mask = np.zeros(NUM_POSSIBLE_MOVES, dtype=np.float32)
    mask[move_indices] = 1.0
    return mask

def move_to_index(move):
    index = 0
    if move.promotion is None:
        index = move.from_square * 64 + move.to_square
    elif move.promotion == chess.KNIGHT:
        index = 4096 + move.to_square
    elif move.promotion == chess.BISHOP:
        index = 4096 + 64 + move.to_square
    elif move.promotion == chess.ROOK:
        index = 4096 + 64*2 + move.to_square
    elif move.promotion == chess.QUEEN:
        index = 4096 + 64*3 + move.to_square
    else:
        raise ValueError(f"Unknown promotion piece type: {move.promotion}")
    return index

# Load Model weights
policy_value_net = PolicyValueNetwork(NUM_POSSIBLE_MOVES)
# dummy input for building network
dummy_input = tf.random.normal((1, 8, 8, NUM_INPUT_PLANES))
policy, value = policy_value_net(dummy_input)

# Replace 'path/to/your/model.weights.h5' with the actual path to your .h5 weights
model_path = "path/to/your/model.weights.h5"
policy_value_net.load_weights(model_path)

# Example usage
board = chess.Board()
input_data = board_to_input(board)
legal_moves_mask = get_legal_moves_mask(board)
input_data = np.expand_dims(input_data, axis=0) # Add batch dimension

policy_output, value_output = policy_value_net(input_data)
policy_output = policy_output.numpy()
value_output = value_output.numpy()
masked_policy_probs = policy_output[0] * legal_moves_mask # Apply legal move mask

# Normalize policy probabilities, make it zero if sum of probabilities is zero.
if np.sum(masked_policy_probs) > 0:
    masked_policy_probs /= np.sum(masked_policy_probs)

print("Policy Output:", masked_policy_probs)
print("Value Output:", value_output)
```

### Citation

If you use this model in your research, please cite it as follows:

```bibtex
@misc{stockzero,
  author = {Nirajan Dhakal},
  title = {StockZero: A Self-Play Reinforcement Learning Chess Engine},
  year = {2025},
  publisher = {Hugging Face},
  journal = {Hugging Face Model Card},
  howpublished = {\url{https://huggingface.co/nirajandhakal/StockZero-v2}}
}
```
