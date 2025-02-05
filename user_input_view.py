import tkinter as tk
from datetime import datetime

import main_linux


class ChatApplication:
    def __init__(self, root, valid_commands=None):
        """
        Initialize the Chat Application in the provided Tkinter root window.
        """
        # Store references to currently displayed messages
        self.displayed_messages = []

        # Colors for Night Mode
        self.BACKGROUND_COLOR = "#2b2b2b"  # Dark background for the app
        self.TEXT_COLOR = "#ffffff"  # White text for readability
        self.MESSAGE_BG_COLOR = "#2b2b2b"  # Matching background to make labels "invisible"

        # Timer variables - to track the start time
        self.start_time = datetime.now()  # Program's execution start time

        # Approximate height of a single message (in pixels)
        self.MESSAGE_HEIGHT = 40

        # Initialize the main window
        self.root = root
        self.valid_commands = valid_commands
        self.setup_window()

    def setup_window(self):
        """
        Set up the main window layout with all components.
        """
        # Configure the root window
        self.root.title("YOUTUBE LIVE PLAYS POKEMON")
        self.root.geometry("700x600")  # Default size
        self.root.resizable(False, True)  # Allows vertical resizing only
        self.root.configure(bg=self.BACKGROUND_COLOR)

        # Add a timer label at the top
        self.timer_label = tk.Label(
            self.root,
            font=("Arial", 30, "bold"),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR,
            pady=10,
        )
        self.timer_label.pack(anchor="n")  # Place timer at the top center

        # Add a keys label below the timer label
        self.keys_label = tk.Label(
            self.root,
            font=("Arial", 15),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR,
            pady=10,
        )
        self.keys_label.pack(anchor="n")  # Place keys label below the timer

        self.update_keys_label()

        # Add a frame to make the chat resizable
        self.chat_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

        # Start the timer
        self.update_timer()

    def calculate_max_messages(self):
        """
        Calculates the maximum number of messages that can fit in the current vertical size of the window.
        """
        current_window_height = self.root.winfo_height()  # Get the window's current height
        available_height = current_window_height - 100  # Subtract non-chat UI height
        # Calculate how many full message containers would fit
        max_messages = max(1, available_height // self.MESSAGE_HEIGHT)
        return max_messages

    def remove_extra_messages(self):
        """
        Removes messages to keep the count within the dynamically calculated MAX_MESSAGES.
        """
        max_messages = self.calculate_max_messages()
        while len(self.displayed_messages) >= max_messages:
            oldest_message = self.displayed_messages.pop(0)  # Remove from the queue
            oldest_message.destroy()  # Remove the widget from display

    def update_timer(self):
        """
        Updates the timer label with the elapsed time since the program started.
        """
        elapsed_time = datetime.now() - self.start_time  # Calculate elapsed time
        total_seconds = int(elapsed_time.total_seconds())

        # Calculate days, hours, minutes, and seconds
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Update the timer label
        self.timer_label.config(
            text=f"Current Playtime: {days}d {hours:02}h {minutes:02}m {seconds:02}s"
        )

        # Schedule the next update in 1 second
        self.root.after(1000, self.update_timer)

    def add_message(self, username, message):
        """
        Adds a new message to the app, with username on the left and their message on the right.
        Removes extra messages if the message count exceeds dynamically calculated MAX_MESSAGES.
        """
        # Create a new container to hold the user's username and message, arranged horizontally
        message_container = tk.Frame(self.chat_frame, bg=self.MESSAGE_BG_COLOR)
        message_container.pack(anchor="w", pady=5, padx=10, fill="x")  # Align Left

        # Add the username label on the left
        username_label = tk.Label(
            message_container,
            text=username,
            font=("Arial", 20, "bold"),
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR,
            width=15,  # Fixed width for alignment
            anchor="w",  # Align text to the left within the label
        )
        username_label.pack(side="left", padx=5)

        # Add the message label on the right
        message_label = tk.Label(
            message_container,
            text=message,
            font=("Arial", 20),
            wraplength=350,  # Prevent long messages from overflowing the window
            bg=self.BACKGROUND_COLOR,
            fg=self.TEXT_COLOR,
            anchor="w",  # Align text to the left within the label
        )
        message_label.pack(side="left", padx=5, fill="x", expand=True)

        # Add the message container to the list of displayed messages
        self.displayed_messages.append(message_container)

        # Remove extra messages if necessary
        self.remove_extra_messages()

    def add_messages_with_delay(self, messages, index=0):
        """
        Recursively add messages with a 1-second delay between each.
        """
        if index < len(messages):  # Check if there are more messages to display
            username, message = messages[index]
            self.add_message(username, message)
            self.root.after(1000, self.add_messages_with_delay, messages, index + 1)

    def on_resize(self, event):
        """
        Event triggered when the window is resized. Adjusts the maximum number of messages dynamically.
        """
        self.remove_extra_messages()

    def update_keys_label(self):
        """
        Updates the label to display all keys of the dictionary.
        """
        keys = ", ".join(self.valid_commands.keys())
        self.keys_label.config(
            text=f"Try typing: {keys}"
        )

# Example usage of the class (e.g., in main_linux)
if __name__ == "__main__":
    root = tk.Tk()

    # Example messages to display
    messages = [
        ("John", "Hello! How's everyone?"),
        ("Jane", "Hi John! I'm doing great!"),
        ("Emma", "Hey team, this app looks awesome!"),
        ("John", "How's the progress on the project?"),
        ("Jane", "It's coming along really well!"),
        ("Emma", "I'll finish it by tomorrow."),
        ("Alex", "Great to hear, everyone!"),
        ("Sophia", "Let's meet to discuss updates."),
        ("John", "Sure, when should we meet?"),
        ("Jane", "How about 2pm?"),
        ("Emma", "2pm works for me."),
        ("Alex", "I'll be there too."),
        ("Sophia", "Perfect, see you all at 2pm!"),
    ]

    # Initialize the ChatApplication class
    app = ChatApplication(root, main_linux.CHAT_TO_WINDOWS_INPUT_MAP)

    # Add messages with a delay
    app.add_messages_with_delay(messages)

    # Start the Tkinter event loop
    root.mainloop()
