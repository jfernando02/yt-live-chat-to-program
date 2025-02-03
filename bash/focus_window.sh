#!/bin/bash

# Set DISPLAY explicitly to ensure graphical environment is accessible
export DISPLAY=:0

# Path to the config.json file
CONFIG_FILE="config.json"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "Error: jq is not installed. Install jq and try again."
  exit 1
fi

# Check if the config.json file exists
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: Config file ($CONFIG_FILE) not found!"
  exit 1
fi

# Extract the search term (title) from config.json
SEARCH_TERM=$(jq -r '.title' "$CONFIG_FILE")

# Validate that the search term was extracted successfully
if [ -z "$SEARCH_TERM" ] || [ "$SEARCH_TERM" == "null" ]; then
  echo "Error: The 'title' field is missing or null in $CONFIG_FILE."
  exit 1
fi

echo "Searching for a window with title: $SEARCH_TERM"

# Find the window ID using the search term from config.json
WINDOW_ID=$(xdotool search --all --name "$SEARCH_TERM" | head -n 1)

# Check if the window was found
if [ -z "$WINDOW_ID" ]; then
  echo "No window found with title: $SEARCH_TERM"
  exit 1
fi

# Activate the detected window
echo "Activating window with ID: $WINDOW_ID"
xdotool windowactivate "$WINDOW_ID"