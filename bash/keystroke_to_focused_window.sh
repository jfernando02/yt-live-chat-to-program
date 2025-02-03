#!/bin/bash

# Set DISPLAY explicitly to ensure graphical environment is accessible
export DISPLAY=:99

# Check if a keystroke is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <keystroke>"
  exit 1
fi

# Read the keystroke argument
KEYSTROKE="$1"

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