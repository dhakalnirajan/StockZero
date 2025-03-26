# StockZero: RL Chess Engine Web Application

![GitHub License](https://img.shields.io/github/license/dhakalnirajan/StockZero?style=for-the-badge&logo=github&logoColor=white&label=License&labelColor=purple&color=orange)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF3F06?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
[![Huggingface](https://img.shields.io/badge/Hugging%20Face-FF3F06?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/nirajandhakal/StockZero-v2)
[![Follow me on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/follow-me-on-HF-sm.svg)](https://huggingface.co/nirajandhakal)

**StockZero** is a robust and scalable web application for playing chess against a powerful Reinforcement Learning (RL) AI engine. Built for production, it combines strategic mastery with tactical acuity, offering a challenging and engaging chess experience.

**Key features include real-time game logging in PGN format to a PostgreSQL database, optimized inference with Redis caching and GPU utilization, versioned model saving, and a streamlined deployment process.**


<video width="60%" height="80%" controls autoplay loop muted playsinline poster="./assets/demo_video_thumbnail.png">
    <source src="./assets/StockZero-v2-gameplay.mp4" type="video/mp4">
    Your browser does not support HTML5 video.
</video>

## Project Structure

```
stockzero/
└───stockzero/                      : Project Root - Core Django settings and URLs.
    │   asgi.py
    │   __init__.py
    │   settings.py
    │   urls.py
    │   wsgi.py
    │
    └───__pycache__/
└───engine/                         : Highly optimized core chess engine components:
    │   __init__.py
    │   mcts.py                     : Production-grade Monte Carlo Tree Search.
    │   model.py                    : PolicyValueNetwork Definition (TensorFlow/Keras).
    │   rl_agent.py                 : Robust Reinforcement Learning Agent (RLEngine).
    │   traditional_engine.py       : Basic traditional engine code.
    │   utils.py                    : Efficient utility functions (board repr, deterministic move encodings).
    │
    └───__pycache__/
└───inference/                      : Production-Ready Inference Engine:
    │   __init__.py
    │   inference_engine.py         : Optimized Inference Engine (caching, GPU utilization).
    │
    └───__pycache__/
└───logs/                             : Dedicated directory for production-grade logging.
└───management/                     : Custom Django Management Commands for training and utilities.
    │   __init__.py
    │
    └───commands/
        │   __init__.py
        │   train_model.py          : Django Management Command for Training.
        │
        └───__pycache__/
└───models/                           : Dedicated directory to store versioned model weights.
└───static/                           : Static files root.
    └───frontend/                     : Frontend app static files.
        ├───css/
        │       styles.css
        │
        └───js/
                chess_gui.js
└───templates/                        : Django templates root.
    └───frontend/                     : Frontend app templates.
            game.html               : Frontend HTML template for game.
└───training/                       : Enhanced and versioned training scripts:
    │   data_utils.py             : Efficient Data Handling for Training pipelines.
    │   __init__.py
    │   self_play.py              : Scalable Self-Play Game Generation with PGN recording.
    │   train_network.py          : GPU-optimized NN Training with checkpointing & logging.
    │
    └───__pycache__/
└───webapp/                           : Production-Ready Django Web Application:
    ├───chessgame/                    : Django app for chess game API (REST API).
    │   │   admin.py
    │   │   apps.py
    │   │   __init__.py
    │   │   models.py               : Database Models - Game Record.
    │   │   serializers.py          : REST API Serializers.
    │   │   urls.py                 : App URLs - API Endpoints.
    │   │   views.py                : Django REST API Views - Real-time Logging, PGN Recording.
    │   │
    │   └───migrations/
    │       │   __init__.py
    │       │
    │       └───__pycache__/
    │
    └───frontend/                     : Django app for optimized Frontend GUI (HTML, CSS, JS).
        │   admin.py
        │   apps.py
        │   __init__.py
        │   urls.py                 : App URLs - Frontend Pages.
        │   views.py                : Django Frontend Views.
        │
        └───static/
        │   └───frontend/
        │       └───css/
        │       └───js/
        │
        └───templates/
            └───frontend/
                    game.html       : Frontend HTML template for game.
.env                                  : Secure storage for environment variables.
.gitattributes
.gitignore
INFERENCE_DOC.md                      : Detailed Inference and API usage documentation.
manage.py                             : Django management script.
manage.sh                             : Bash script for server management tasks.
manage_logs.sh                        : Bash script for log management.
README.md                             : Project documentation (this file).
requirements.txt                      : Python dependencies (production ready).
setup_server.sh                       : Bash script for PostgreSQL & Redis setup.
TRAINING_DOC.md                       : Comprehensive Training documentation.
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
