from datetime import datetime
import queue
import threading
import json
from chat_downloader import ChatDownloader

import input_to_program_linux
import user_input_view
import tkinter as tk

message_queue = queue.Queue()
display_queue = queue.Queue()

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
    current_time = datetime.now().strftime("%H:%M:%S")
    chat = ChatDownloader(cookies="./cookies.txt").get_chat(url, start_time=current_time)

    # Note CMD only supports ASCII characters, so it will display non-ASCII characters as "?"
    print('\n Messages:')
    for message in chat:
        chat.print_formatted(message)
        potential_input = message['message']
        if valid_move_command(potential_input):
            message_queue.put(CHAT_TO_WINDOWS_INPUT_MAP[potential_input])
            display_queue.put([message['author']['name'], message['message']])

def processor_thread():
    """
    Processes messages from the shared queue.
    Validates and executes valid messages.
    """
    virtual_display = input_to_program_linux.VirtualDisplayManager(display_number=99)

    while True:
        # Wait for a message to arrive in the queue
        try:
            message = message_queue.get(timeout=1)  # Timeout prevents getting stuck if there are no messages
        except queue.Empty:
            continue

        # Process the message (execute)
        input_to_program_linux.main(title, message, virtual_display)

        # Mark the task as done
        message_queue.task_done()

def valid_move_command(message):
    """
    Validates and handles a move command.
    If valid, adds the command to the queue

    Args:
        message (str): The user's input message.

    Returns:
        bool: True if the message is valid and processed successfully, False otherwise.
    """
    try:
        action = message.lower()
        if action in CHAT_TO_WINDOWS_INPUT_MAP:
            return True
        else:
            return False

    except Exception as e:
        # Catch any unexpected errors (e.g., malformed inputs)
        print(f"Error handling command: {e}")
        return False

def start_gui():
    """
    Initialize the GUI (ChatApplication) and integrate the display queue.
    """

    def poll_display_queue():
        """
        Polls the display_queue for new messages and adds them to the user_input_view (ChatApplication).
        """
        try:
            while not display_queue.empty():
                # Fetch a new message from the display queue
                username, message = display_queue.get_nowait()

                # Add the message to the ChatApplication
                app.add_message(username, message)

                # Mark message as processed
                display_queue.task_done()

        except queue.Empty:
            pass  # No new messages in the display queue

        # Schedule the next poll in 100ms
        root.after(100, poll_display_queue)

    # Create main Tkinter window
    root = tk.Tk()

    # Initialize the ChatApplication instance
    app = user_input_view.ChatApplication(root)

    # Start polling for new messages from the display queue
    root.after(100, poll_display_queue)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    # Create listener and processor threads
    listener = threading.Thread(target=listener_thread, daemon=True)
    processor = threading.Thread(target=processor_thread, daemon=True)

    # Start the threads
    listener.start()
    processor.start()

    start_gui()