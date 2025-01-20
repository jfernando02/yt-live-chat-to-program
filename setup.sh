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

echo "Installing tkinter..."
sudo apt-get install python3-tk

echo "Setup complete!"