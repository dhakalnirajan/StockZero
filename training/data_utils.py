import pickle

def save_training_data(game_histories, filename="self_play_games.pkl"):
    """Saves game histories to a pickle file."""
    with open(filename, "wb") as f:
        pickle.dump(game_histories, f)
    print(f"Training data saved to {filename}")

def load_training_data(filename="self_play_games.pkl"):
    """Loads game histories from a pickle file."""
    try:
        with open(filename, "rb") as f:
            game_histories = pickle.load(f)
        print(f"Training data loaded from {filename}")
        return game_histories
    except FileNotFoundError:
        print(f"Error: Training data file not found: {filename}")
        return []

if __name__ == "__main__":
    # Example usage (for testing data saving/loading)
    example_data = [("fen1", [0.1, 0.9], 1), ("fen2", [0.5, 0.5], -1)] # Dummy data
    save_training_data([example_data], "example_training_data.pkl")
    loaded_data = load_training_data("example_training_data.pkl")
    print(f"Loaded data example: {loaded_data}")