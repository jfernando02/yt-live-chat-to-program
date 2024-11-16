#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install system-level dependencies
echo "Installing Xvfb..."
sudo apt-get install -y xvfb

# Install xdotool
echo "Installing xdotool..."
sudo apt-get install -y xdotool

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"