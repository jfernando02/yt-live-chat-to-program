#!/bin/bash

# Set DISPLAY to the virtual display
export DISPLAY=:10.0

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
SEARCH_TERM=$(jq -r '.TITLE' "$CONFIG_FILE")

# Validate that the search term was extracted successfully
if [ -z "$SEARCH_TERM" ] || [ "$SEARCH_TERM" == "null" ]; then
  echo "Error: The 'TITLE' field is missing or null in $CONFIG_FILE."
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