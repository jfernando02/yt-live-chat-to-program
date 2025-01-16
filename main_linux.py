import time
import queue
import threading
import json
from chat_downloader import ChatDownloader

import input_to_program_linux

message_queue = queue.Queue()

CHAT_TO_WINDOWS_INPUT_MAP = {
    "a": "c",
    "b": "v",
    "left": "a",
    "right": "d",
    "up": "w",
    "down": "s",
    "select": "z",
    "start": "x"
}

# Load the configuration file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Access the variables
title = config.get("TITLE", "Default Title")  # Default if not found
url = config.get("URL", "https://default.url")  # Default if not found

def listener_thread():
    current_time = time.time()
    chat = ChatDownloader(cookies="./cookies.txt").get_chat(url, start_time=current_time)

    def format_message(message_dictionary, add_name):  # FORMAT: <author>:   <message> or <message>
        formatted_message_string = message_dictionary['message']

        if add_name:
            author = message_dictionary['author']
            formatted_message_string = author['name'] + ':   ' + formatted_message_string
        return formatted_message_string

    # Note CMD only supports ASCII characters, so it will display non-ASCII characters as "?"
    print('\n Messages:')
    for message in chat:
        chat.print_formatted(message)
        potential_input = format_message(message, False)
        handle_move_command(potential_input)

def processor_thread():
    """
    Processes messages from the shared queue.
    Validates and executes valid messages.
    """
    while True:
        # Wait for a message to arrive in the queue
        try:
            message = message_queue.get(timeout=1)  # Timeout prevents getting stuck if there are no messages
        except queue.Empty:
            continue

        # Process the message (execute)
        input_to_program_linux.main(title, message)

        # Mark the task as done
        message_queue.task_done()

def handle_move_command(message):
    """
    Validates and handles a !move command.
    If valid, adds the command to the queue `n` times (where n is specified, defaults to 1 if omitted).

    Args:
        message (str): The user's input message.

    Returns:
        bool: True if the message is valid and processed successfully, False otherwise.
    """
    # Ensure the command starts with "!move"
    if not message.startswith("!move"):
        return False  # Invalid command

    try:
        # Extract the part after "!move" and strip extra spaces
        command_body = message[len("!move"):].strip()

        # Handle the case where only an action (e.g., "a") is provided
        if command_body.isalpha() and command_body.lower() in CHAT_TO_WINDOWS_INPUT_MAP:
            action = command_body.lower()
            count = 1  # Default to 1 if no number is provided
        else:
            # Validate the pattern: start with a number followed by a single letter
            if len(command_body) < 2:
                return False  # Not enough characters after "!move"

            # Extract the count (number) and the action (character)
            count_str = command_body[0]
            action = command_body[1:].lower()

            # Ensure we extracted a valid number (or default to 1) and a valid action
            if not count_str.isdigit() or action not in CHAT_TO_WINDOWS_INPUT_MAP:
                return False

            count = int(count_str)

        # Add the action to the queue `count` number of times
        for _ in range(count):
            message_queue.put(CHAT_TO_WINDOWS_INPUT_MAP[action])

        print(f"Added '{action}' to the queue {count} times.")
        return True

    except Exception as e:
        # Catch any unexpected errors (e.g., malformed inputs)
        print(f"Error handling command: {e}")
        return False


if __name__ == "__main__":
    # Create listener and processor threads
    listener = threading.Thread(target=listener_thread, daemon=True)
    processor = threading.Thread(target=processor_thread, daemon=True)

    # Start the threads
    listener.start()
    processor.start()

    # Keep the main thread alive
    listener.join()
    processor.join()