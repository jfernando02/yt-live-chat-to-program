import argparse
import subprocess
import time
import shlex
import os

class VirtualDisplayManager:
    def __init__(self, display_number):
        self.display_number = display_number
        self.display_env = f":{display_number}"

        # Start Xvfb as a virtual display
        self.xvfb_process = subprocess.Popen(shlex.split(f"Xvfb {self.display_env}"),
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

        # Set the DISPLAY environment variable
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

    def send_keystroke(self, partial_title, keystroke):
        """
        Send keystroke into the focused window.
        :param keystroke: The keystroke to send
        :type keystroke: str
        """
        subprocess.run(["./bash/keystroke_to_focused_window.sh", partial_title, keystroke], check=True)

def main(title=None, keystroke=None, virtual_display=None):
    if virtual_display is None:
        virtual_display = VirtualDisplayManager(display_number=99)

    retry_count = 3
    # Type some text into the application window
    for attempt in range(retry_count):
        try:
            virtual_display.send_keystroke(partial_title=title, keystroke=keystroke)
            break
        except Exception as e:
            print(f"Error sending keystroke on attempt {attempt + 1}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a virtual display manager and interact with application windows.")
    parser.add_argument(
        "-t", "--title",
        required=True,
        help="The partial title of the application window to focus (e.g. 'InputTest.txt - Terminal')."
    )
    parser.add_argument(
        "-k", "--keystroke",
        required=True,
        help="The keystroke to send (e.g. 'a', 'Shift+a')."
    )
    args = parser.parse_args()
    main(args.title, args.keystroke)