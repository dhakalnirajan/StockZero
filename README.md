# StockZero: RL Chess Engine Web Application

**StockZero** is a robust and scalable web application for playing chess against a powerful Reinforcement Learning (RL) AI engine. Built for production, it combines strategic mastery with tactical acuity, offering a challenging and engaging chess experience.

**Key features include real-time game logging in PGN format to a PostgreSQL database, optimized inference with Redis caching and GPU utilization, versioned model saving, and a streamlined deployment process.**

## Project Structure

```
stockzero/
stockzero/ : Project Root - Core Django settings and URLs.
engine/ : Highly optimized core chess engine components:
model.py : PolicyValueNetwork Definition (TensorFlow/Keras).
mcts.py : Production-grade Monte Carlo Tree Search.
rl_agent.py : Robust Reinforcement Learning Agent (RLEngine).
utils.py : Efficient utility functions (board repr, deterministic move encodings).
training/ : Enhanced and versioned training scripts:
self_play.py : Scalable Self-Play Game Generation with PGN recording.
train_network.py : GPU-optimized Neural Network Training script with checkpointing & logging.
data_utils.py : Efficient Data Handling for Training pipelines.
inference/ : Production-Ready Inference Engine:
inference_engine.py : Optimized Inference Engine (caching, GPU utilization).
webapp/ : Production-Ready Django Web Application:
chessgame/ : Django app for chess game API (REST API) - Robust & Scalable API with game logging to PostgreSQL DB.
frontend/ : Django app for optimized Frontend GUI (HTML, CSS, JS).
management/ : Custom Django Management Commands for training and utilities.
logs/ : Dedicated directory for production-grade logging to files (engine, webapp logs).
.env : Secure storage for environment variables (database, Redis credentials, secret key).
models/ : Dedicated directory to store versioned and trained model weights (using StockZero-{year}-{month-day}.weights.h5 naming convention).
manage.py : Django management script.
requirements.txt: Python dependencies (production ready).
README.md : Project documentation (this file).
TRAINING_DOC.md : Comprehensive Training documentation.
INFERENCE_DOC.md: Detailed Inference and API usage documentation.
DEPLOYMENT_DOC.md: Production-grade Django deployment documentation (Nginx, Gunicorn, PostgreSQL, Redis).
manage.sh : Bash script for automating common server management tasks (setup, runserver, logging, training).
setup_server.sh : Bash script to automate PostgreSQL and Redis setup on a Linux server.
manage_logs.sh : Bash script for log management (show, archive, combine logs).
```

## Key Production Features

* **Robust and Scalable REST API:** Django REST Framework API for efficient communication between frontend and backend, with rate limiting implemented for security.
* **Real-time PGN Game Logging:**  Gameplay is logged in real-time to a PostgreSQL database in PGN format, capturing complete game history and results for analysis and record-keeping.
* **Optimized Inference Engine:** Utilizes Redis caching and GPU acceleration for lightning-fast AI move generation, ensuring responsiveness under load.
* **Versioned Model Saving:** Trained models are saved with versioned filenames (`StockZero-{year}-{month-day}.weights.h5`) in a dedicated `models/` directory, facilitating model management and rollbacks.
* **Production-Grade Logging:** Comprehensive logging to separate files for engine and webapp components, aiding in monitoring and debugging in production environments.
* **PostgreSQL Database:** Uses PostgreSQL as the production-ready database backend for reliability, scalability, and data integrity.
* **Redis Caching:** Leverages Redis for high-performance caching of AI move lookups, drastically reducing latency and server load during gameplay.
* **GPU Utilization:** Designed for optimal GPU utilization during both training and inference with TensorFlow, ensuring maximum performance on GPU-enabled servers.
* **Enhanced Security:** Includes security best practices in `settings.py` (HTTPS settings, SECRET_KEY management, etc.) and rate limiting to protect the API.
* **Simplified Deployment:** Comprehensive `DEPLOYMENT_DOC.md`, `manage.sh`, and `setup_server.sh` scripts facilitate easy and repeatable production deployment on Linux servers using Nginx, Gunicorn, PostgreSQL, and Redis.
* **Automated Tasks:** `manage.sh` and custom Django management command (`train_model`) automate common tasks like setup, training, and server management.
* **Clear Documentation:** Comprehensive documentation across `README.md`, `TRAINING_DOC.md`, `INFERENCE_DOC.md`, and `DEPLOYMENT_DOC.md` provides detailed guidance for all aspects of the project.

## Setup and Run (Production Ready)

1. **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd stockzero
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Place your trained model weights:**
    * Ensure your trained model weights file (e.g., `rl_chess_model.weights.h5` or a versioned model file like `StockZero-2025-03-24.weights.h5`) is in the `stockzero/models/` directory.
    * Verify the model loading path in `engine/__init__.py` (`MODEL_WEIGHTS_FILE` constant).

5. **Configure Environment Variables:**
    * Create a `.env` file in the `stockzero/` root directory.
    * Set essential production environment variables (e.g., `DJANGO_SECRET_KEY`, database credentials `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `REDIS_URL`, `DJANGO_ALLOWED_HOSTS`). Refer to `.env` file example provided in the codebase and `DEPLOYMENT_DOC.md` for details.

6. **Set up PostgreSQL and Redis:**
    * Use `./setup_server.sh` script on a Linux server to automate PostgreSQL and Redis installation and basic configuration.
    * Alternatively, manually set up PostgreSQL and Redis based on your server environment.
    * **Important:** Ensure PostgreSQL database and user are created, and Redis server is running.

7. **Run database migrations:**

    ```bash
    ./manage.sh migrate
    ```

    **This step is critical to create the PostgreSQL database tables for game records.**

8. **Collect static files:**

    ```bash
    ./manage.sh collectstatic
    ```

    **(Important for production deployment - prepares static files for efficient serving)**

9. **Start the Django development server (for testing):**

    ```bash
    ./manage.sh runserver
    ```

10. **Access the application (development server):**
    Open your browser to `http://127.0.0.1:8000/`

11. **For Production Deployment:** Follow the comprehensive deployment steps in `DEPLOYMENT_DOC.md` to set up Gunicorn, Nginx, and configure a production-ready server environment.

## Training the RL Model

See detailed training instructions in `TRAINING_DOC.md`. Use the Django management command:

```bash
python manage.py train_model --games <num_games> --epochs <num_epochs> --simulations <num_simulations>
```

<br>

**Example**: python manage.py train_model --games 100 --epochs 20 --simulations 100

<br>

## Inference and API Usage

See detailed inference and API usage instructions in `INFERENCE_DOC.md`. Use the Django management command:

```bash
python manage.py runserver
```

## Management Scripts

Use `manage.sh` and custom Django management commands for streamlined project management. See `manage.sh` help for usage instructions.
