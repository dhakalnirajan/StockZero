# StockZero RL Chess Engine - Training Documentation

This document provides a comprehensive guide to training the production-grade Reinforcement Learning (RL) model for the StockZero chess engine, emphasizing scalability, efficiency, and best practices.

## 1. Prerequisites

* **Hardware:**
  * **High-Performance GPU(s) (Required for Production Training):** Training a strong chess AI for production requires powerful GPUs to handle the massive computations. Consider using multi-GPU setups or cloud GPU instances (AWS EC2, Google Cloud TPUs/GPUs, Azure VMs with GPUs).
  * Large RAM (64GB+ recommended, scale with network size and training data volume).
  * High-speed storage (SSD NVMe) for efficient data loading and checkpoint saving.

* **Software:**
  * Ubuntu Server or similar Linux distribution (recommended for production).
  * Python 3.9+ (for optimized performance).
  * TensorFlow 2.10+ (or a recent PyTorch version, if adapting the codebase to PyTorch).
  * CUDA Toolkit and cuDNN (latest compatible versions for your GPUs).
  * python-chess library (latest version).
  * Django (required for project structure and management commands, even for training).
  * Redis (for caching - optional during training, but helpful for data pipelines).
  * Virtualenv or Conda for environment isolation.

## 2. Production Training Process Overview

The production training process for StockZero is designed for scalability and efficiency, focusing on generating large datasets and training robust models. Key stages include:

1. **Massive Self-Play Game Generation (Scalable):** Leverage distributed systems or multi-processing to generate a massive dataset of self-play games. Aim for millions or tens of millions of games for a production-level engine. Use `training/self_play.py` and consider parallelization strategies.
2. **Efficient Data Storage and Management:** Implement efficient data pipelines for storing, loading, and preprocessing self-play game data. Consider using optimized data formats (e.g., TFRecord if using TensorFlow) and data sharding for parallel processing. Utilize `training/data_utils.py` for data management.
3. **GPU-Accelerated Distributed Training (Scalable):**  Utilize multi-GPU training or distributed training strategies (e.g., TensorFlow's `tf.distribute.Strategy`, Horovod) to parallelize the neural network training across multiple GPUs.  Optimize training scripts in `training/train_network.py` for GPU efficiency and scalability.
4. **Regular Model Evaluation and Checkpointing:** Implement robust model evaluation procedures to track training progress and identify overfitting or performance degradation.  Use checkpointing (already implemented in `train_network.py`) to save model weights periodically and enable training resumption and model versioning.
5. **Iterative Training Cycles:** Run iterative training cycles, continuously generating new self-play data with improved models and retraining the neural network to refine its policy and value functions.
6. **Versioned Model Saving:** Save trained models with versioned filenames (e.g., `StockZero-{year}-{month-day}.weights.h5`) and manage them in the `models/` directory to track training iterations and enable rollbacks if needed.

## 3. Training Scripts (Production Enhanced)

* **`training/self_play.py` (Production Ready Self-Play):**
  * Function `self_play_game(num_simulations, game_index)`: Generates a single self-play game, now with PGN recording to files, enhanced logging, and clear game progress output. Consider adapting this for parallel game generation (e.g., using multiprocessing or distributed task queues) to scale up self-play data creation.
  * Function `create_policy_targets_from_mcts_visits(root_node)`: Utility for converting MCTS visit counts to policy targets.
  * Example `if __name__ == "__main__":` block provides an example of how to generate and save a small number of games for testing.

* **`training/train_network.py` (Production-Grade Training):**
  * Function `train_step(model, board_inputs, policy_targets, value_targets, optimizer)`: Performs a single GPU-accelerated training step with gradient tape optimization (TensorFlow).
  * Function `train_network(model, game_histories, optimizer, epochs=10, batch_size=32, checkpoint_path=None, checkpoint_freq=5)`: Orchestrates the training loop, now with detailed per-epoch logging, average epoch loss reporting, and periodic model checkpoint saving.
  * Example `if __name__ == "__main__":` block shows how to load training data from files (replace with your actual data loading pipeline) and initiates the training process with checkpointing.

* **`training/data_utils.py` (Data Handling Utilities):**
  * Function `save_training_data(game_histories, filename="self_play_games.pkl")`: Saves game histories to pickle files (you might want to explore more efficient formats like TFRecord for large datasets).
  * Function `load_training_data(filename="self_play_games.pkl")`: Loads game histories from pickle files (adapt for your data format).  For production, consider using data pipelines that stream data efficiently and avoid loading entire datasets into memory at once, especially for very large training datasets.

## 4. Running Production Training (Django Management Command)

Use the Django management command `train_model` to initiate production training:

```bash
python manage.py train_model --games <num_games> --epochs <num_epochs> --simulations <num_simulations>
```

* `--games <num_games>`: Number of self-play games to generate per training iteration. For production training, increase this significantly (e.g., --games 1000, --games 10000 or more depending on your scale and resources).

* `--epochs <num_epochs>`: Number of training epochs per iteration. Adjust epochs based on your evaluation metrics and training convergence behavior.

* `--simulations <num_simulations>`: Number of MCTS simulations per move during self-play game generation. Increase simulations for stronger self-play, but it will also increase training time. Find a good balance.

**Example Command`**:

```bash
python manage.py train_model --games 1000 --epochs 10 --simulations 2000
```

## 5. GPU Optimization and CUDA Optimization

* GPU is Critical: GPU acceleration is essential for production-level StockZero training. Ensure you are training on machines with powerful NVIDIA GPUs and that TensorFlow is correctly configured to utilize them.

* `tf.device('/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0')`: Explicit GPU device placement is used in train_network.py and `inference_engine.py` to guide TensorFlow to use the GPU if available.

Batch Size and GPU Memory: Optimize `batch_size` in `train_network.py` to maximize GPU utilization without causing out-of-memory errors. Experiment to find the largest batch size that fits in your GPU memory.

Data Prefetching (`tf.data.AUTOTUNE`): The `tf.data.Dataset` pipeline uses `prefetch(tf.data.AUTOTUNE) to improve data loading efficiency and keep the GPU busy during training.

Mixed Precision Training (Advanced): For further GPU optimization and potentially faster training, consider implementing mixed precision training (e.g., using TensorFlow's `tf.keras.mixed_precision.Policy`). This can reduce memory usage and speed up computations on compatible GPUs.

Distributed Training (Scalability): For very large-scale training, explore distributed training strategies (TensorFlow Distributed Training, Horovod, etc.) to distribute the training workload across multiple GPUs or machines, further accelerating training and enabling the use of larger models and datasets.

## 6. Model Checkpointing and Versioning

* **Checkpoint Directory**: Model checkpoints are saved in the `training/checkpoints/` directory during training.

* **Periodic Checkpoints**: Checkpoints are saved every `checkpoint_freq` epochs (you can adjust `checkpoint_freq` in `train_network.py`).

* **Versioned Model Weights**: Final trained model weights are saved with versioned filenames (e.g., `StockZero-{year}-{month-day}.weights.h5`) in the `models/` directory, managed by the train_model command.

## 7. Production Data Pipeline Considerations

* Scalable Data Storage: For large-scale self-play data, consider using cloud-based object storage (e.g., AWS S3, Google Cloud Storage, Azure Blob Storage) to store and manage game history files efficiently.

* Efficient Data Format (TFRecord): For very large datasets, explore using TFRecord format for storing training data. TFRecord is a binary format optimized for TensorFlow data pipelines and allows for efficient data streaming and parallel loading.

* Data Sharding: Shard your training data across multiple files to enable parallel data loading and processing in distributed training scenarios.

* Data Augmentation (Advanced): Consider data augmentation techniques (e.g., rotating or mirroring board positions) to increase the size and diversity of your training data, potentially improving model generalization and robustness.
