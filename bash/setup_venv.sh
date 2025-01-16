#!/bin/bash

# Name of the virtual environment directory
VENV_DIR="venv"

echo "Setting up Python virtual environment..."

# Step 1: Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python3 is not installed. Please install it and try again."
    exit 1
fi

# Step 2: Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "Error: pip3 is not installed. Please install it and try again."
    exit 1
fi

# Step 3: Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment ($VENV_DIR)..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create the virtual environment."
        exit 1
    fi
else
    echo "Virtual environment ($VENV_DIR) already exists. Skipping creation step."
fi

# Step 4: Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate the virtual environment."
    exit 1
fi

# Step 5: Install required dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip  # Upgrade pip to the latest version
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "Dependencies installed successfully!"
    else
        echo "Error: Failed to install dependencies."
        deactivate
        exit 1
    fi
else
    echo "Warning: requirements.txt not found. Skipping package installation."
fi

# Final Step: Notify the user
echo "Virtual environment setup complete."
echo "To activate it in the future, run: source $VENV_DIR/bin/activate"
echo "To deactivate, simply run: deactivate"