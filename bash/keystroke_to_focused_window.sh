#!/bin/bash

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

# Send the keystroke to the focused window
xdotool key --window "$FOCUSED_WINDOW" "$KEYSTROKE"