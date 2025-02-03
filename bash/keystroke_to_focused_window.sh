#!/bin/bash

export DISPLAY=:10.0

# Check if a search term (title) is provided as the first argument
if [ -z "$1" ]; then
  echo "Usage: $0 <search_term>"
  exit 1
fi

# Use the first argument as the search term
SEARCH_TERM="$1"

# Validate that the search term is not empty
if [ -z "$SEARCH_TERM" ]; then
  echo "Error: The search term is empty."
  exit 1
fi

# Find the window ID using the search term from config.json
WINDOW_ID=$(xdotool search --all "$SEARCH_TERM" | head -n 1)

# Check if the window was found
if [ -z "$WINDOW_ID" ]; then
  echo "No window found with title: $SEARCH_TERM"
  exit 1
fi

# Activate the detected window
echo "Activating window with ID: $WINDOW_ID"
xdotool windowactivate "$WINDOW_ID"

# Check if a keystroke is provided
if [ -z "$2" ]; then
  echo "Usage: $0 <keystroke>"
  exit 1
fi

# Read the keystroke argument
KEYSTROKE="$2"

# Log the current focus (for debugging)
FOCUSED_WINDOW=$(xdotool getwindowfocus)
if [ -z "$FOCUSED_WINDOW" ]; then
  echo "No window is currently in focus."
  exit 1
fi

echo "Focused window ID: $FOCUSED_WINDOW"

# Press and hold the keystroke for 0.15 seconds
xdotool keydown --window "$FOCUSED_WINDOW" "$KEYSTROKE"
sleep 0.15  # Hold the key for 0.15 seconds
xdotool keyup --window "$FOCUSED_WINDOW" "$KEYSTROKE"
sleep 0.15 # Add additional sleep