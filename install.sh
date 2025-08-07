#!/bin/bash

# This script automates the installation of required libraries for the Miss Gracy Baby content generation web application.

# --- Configuration ---
PYTHON_CMD="python3" # Use "python" if your system uses that for Python 3
REQUIREMENTS_FILE="requirements.txt"

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

echo_message "Starting the installation process..."

# 1. Check for Python
echo "[1/2] Checking for Python 3..."
if ! command_exists $PYTHON_CMD; then
    echo "ERROR: Python 3 is not installed or not in the system's PATH."
    echo "Please install Python 3 to continue: https://www.python.org/downloads/"
    exit 1
fi
echo "Python 3 found: $($PYTHON_CMD --version)"

# 2. Check for tkinter
echo_message "[2/3] Checking for tkinter..."
if ! $PYTHON_CMD -c "import tkinter" >/dev/null 2>&1; then
    echo "WARNING: tkinter is not installed. It is required for the GUI."
    echo "Please install it using your system's package manager."
    echo "For Debian/Ubuntu: sudo apt-get install python3-tk"
    echo "For Fedora/CentOS: sudo dnf install python3-tkinter"
    # Optionally, you could exit here if tkinter is strictly required
    # exit 1
else
    echo "tkinter is already installed."
fi

# 3. Install Dependencies
echo_message "[3/3] Installing required libraries from $REQUIREMENTS_FILE..."
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

echo_message "Installation complete!"
