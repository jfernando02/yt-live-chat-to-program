#!/bin/bash

# Check that a title was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <partial_window_title>"
  exit 1
fi

# Find and focus window
WINDOW_ID=$(xdotool search --onlyvisible --name "$1")
if [ -z "$WINDOW_ID" ]; then
  echo "No visible window found with title: $1"
  exit 1
fi

xdotool windowactivate "$WINDOW_ID"