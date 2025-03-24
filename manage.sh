#!/bin/bash

# --- Script Configuration ---
PROJECT_ROOT=$(dirname "$(readlink -f "$0")")
VENV_DIR="$PROJECT_ROOT/venv"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"
MANAGE_PY="$PROJECT_ROOT/manage.py"
TRAIN_SCRIPT="$PROJECT_ROOT/training/train_network.py" # Point to training script in training/ directory

# --- Functions ---

function create_venv() {
  echo "Creating virtual environment in $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
  if [ $? -eq 0 ]; then
    echo "Virtual environment created successfully."
  else
    echo "Error creating virtual environment. Please check if python3-venv is installed."
    exit 1
  fi
}

function activate_venv() {
  source "$VENV_DIR/venv/bin/activate"
  if [ $? -eq 0 ]; then
    echo "Virtual environment activated."
  else
    echo "Error activating virtual environment."
    exit 1
  fi
}

function install_dependencies() {
  if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: requirements.txt file not found at $REQUIREMENTS_FILE"
    exit 1
  fi
  echo "Installing dependencies from $REQUIREMENTS_FILE..."
  pip install -r "$REQUIREMENTS_FILE"
  if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
  else
    echo "Error installing dependencies. Check requirements.txt and your pip installation."
    exit 1
  fi
}

function run_migrations() {
  echo "Running database migrations..."
  python "$MANAGE_PY" migrate
  if [ $? -eq 0 ]; then
    echo "Database migrations completed."
  else
    echo "Error running database migrations. Check database settings and migrations files."
    exit 1
  fi
}

function collect_static() {
  echo "Collecting static files..."
  python "$MANAGE_PY" collectstatic --noinput
  if [ $? -eq 0 ]; then
    echo "Static files collected."
  else
    echo "Error collecting static files. Check static file settings."
    exit 1
  fi
}

function run_dev_server() {
  echo "Starting Django development server..."
  python "$MANAGE_PY" runserver 0.0.0.0:8000 # Bind to 0.0.0.0 to access from network if needed
}

function stop_dev_server() {
  echo "Stopping Django development server..."
  #  Simple method: find process and kill (less graceful, but works for dev server)
  PID=$(lsof -ti:8000) # Find process ID listening on port 8000
  if [ -n "$PID" ]; then
    kill "$PID"
    echo "Development server stopped (killed process $PID)."
  else
    echo "Development server not found running on port 8000."
  fi
}

function run_training() {
  if [ ! -f "$TRAIN_SCRIPT" ]; then
    echo "Error: Training script not found at $TRAIN_SCRIPT"
    exit 1
  fi
  echo "Running RL model training script: $TRAIN_SCRIPT..."
  python "$TRAIN_SCRIPT"
}


# --- Main Script Logic ---

if [ -z "$1" ]; then
  echo "Usage: $0 <command>"
  echo "Commands: setup | runserver | stopserver | migrate | collectstatic | train | help"
  exit 1
fi

COMMAND="$1"

case "$COMMAND" in
  setup)
    create_venv
    activate_venv
    install_dependencies
    run_migrations
    collect_static
    echo "Setup complete. Virtual environment created and activated. Dependencies installed."
    ;;
  runserver)
    activate_venv
    run_dev_server
    ;;
  stopserver)
    stop_dev_server
    ;;
  migrate)
    activate_venv
    run_migrations
    ;;
  collectstatic)
    activate_venv
    collect_static
    ;;
  train)
    activate_venv
    run_training
    ;;
  help)
    echo "Usage: $0 <command>"
    echo "Commands:"
    echo "  setup         : Create and activate virtual environment, install dependencies, run migrations, collect static files."
    echo "  runserver     : Start the Django development server."
    echo "  stopserver    : Stop the Django development server."
    echo "  migrate       : Run database migrations."
    echo "  collectstatic : Collect static files for deployment."
    echo "  train         : Run the RL model training script (if configured)."
    echo "  help          : Show this help message."
    ;;
  *)
    echo "Error: Unknown command '$COMMAND'. Use 'help' for valid commands."
    exit 1
    ;;
esac

exit 0