from pywinauto import Application
from pywinauto import Desktop
from pywinauto import keyboard

def send_input_to_pokemon(key):
    # Locate the mgba application by its title
    try:
        # Use the Desktop object to find all windows with the title "POKEMON RED"
        mgba_window = Desktop(backend="win32").window(title_re=".*POKEMON RED.*")
        if mgba_window.exists(timeout=5):
            # Connect to the mgba application
            app = Application(backend="win32").connect(title_re=".*POKEMON RED.*")

            # Set focus to the mgba window
            mgba_window.set_focus()

            # Send keystrokes to the mgba application
            keyboard.send_keys(f"{{{key} down}}")
            keyboard.send_keys(f"{{{key} up}}")
        else:
            print("mgba window not found.")
    except Exception as e:
        print(f"An error occurred: {e}")