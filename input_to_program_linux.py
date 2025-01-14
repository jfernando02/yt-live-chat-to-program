import subprocess
import time
import shlex

class VirtualDisplayManager:
    def __init__(self, display_number):
        self.display_number = display_number
        self.display_env = f":{display_number}"

        # Start Xvfb as a virtual display
        self.xvfb_process = subprocess.Popen(shlex.split(f"Xvfb {self.display_env}"),
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

        # Set the DISPLAY environment variable
        import os
        os.environ["DISPLAY"] = self.display_env

        # Allow some time for Xvfb to initialize
        time.sleep(2)

    def run_application(self, command):
        """
        Run the application in the virtual display.
        :param command: Shell command to run the application
        :type command: str
        """
        subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Allow some time for the application to start
        time.sleep(2)

    def focus_window_by_partial_title(self, partial_title):
        """
        Focus the application window by a portion of its title.
        :param partial_title: A substring of the title of the window to focus
        :type partial_title: str
        """
        # Find the window ID(s) that contain the partial title
        window_id_command = f"xdotool search --name {partial_title}"
        window_ids = subprocess.check_output(shlex.split(window_id_command)).decode().strip().split('\n')

        if not window_ids:
            raise Exception(f"No visible window found containing title: {partial_title}")

        # Focus the first matched window
        focus_command = f"xdotool windowactivate {window_ids[0]}"
        subprocess.run(shlex.split(focus_command))

    def type_text(self, text):
        """
        Type text into the focused window.
        :param text: The text to type
        :type text: str
        """
        type_command = f"xdotool type \"{text}\""
        subprocess.run(shlex.split(type_command))

def main():
    virtual_display = VirtualDisplayManager(display_number=99)

    # Focus the application window by its title
    virtual_display.focus_window_by_partial_title("InputTest.txt")

    # Type some text into the application window
    virtual_display.type_text("Hello, world!")

if __name__ == "__main__":
    main()