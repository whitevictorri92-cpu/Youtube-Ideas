#!/bin/bash

# This script automates the setup and launch of the Miss Gracy Baby content generation web application.

# --- Configuration ---
PYTHON_CMD="python3" # Use "python" if your system uses that for Python 3
REQUIREMENTS_FILE="requirements.txt"
APP_SCRIPT="web/app.py"

# --- Functions ---

# Function to print messages
echo_message() {
    echo "--------------------------------------------------"
    echo "$1"
    echo "--------------------------------------------------"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Main Script ---

echo_message "Starting the Miss Gracy Baby Content Generator..."

# 1. Check for Python
echo "[1/3] Checking for Python 3..."
if ! command_exists $PYTHON_CMD; then
    echo "ERROR: Python 3 is not installed or not in the system's PATH."
    echo "Please install Python 3 to continue: https://www.python.org/downloads/"
    exit 1
fi
echo "Python 3 found: $($PYTHON_CMD --version)"

# 2. Install Dependencies
echo_message "[2/3] Installing required libraries..."
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "ERROR: '$REQUIREMENTS_FILE' not found. Cannot install dependencies."
    exit 1
fi

$PYTHON_CMD -m pip install -r "$REQUIREMENTS_FILE"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python libraries. Please check your pip configuration and try again."
    exit 1
fi
echo "Libraries installed successfully."

# 3. Run the Web Application
echo_message "[3/3] Launching the web application..."

if [ ! -f "$APP_SCRIPT" ]; then
    echo "ERROR: Application script '$APP_SCRIPT' not found."
    exit 1
fi

$PYTHON_CMD "$APP_SCRIPT"

echo "Application has been started. Access it at http://127.0.0.1:5000"
