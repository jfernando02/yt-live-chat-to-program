import ctypes
import time

from chat_downloader import ChatDownloader
from random import randint
from datetime import datetime

from pywinauto.findwindows import enum_windows
from sympy.strategies.core import switch

import input_to_pokemon


def main():
    url = input('   Enter the YouTube URL: ')
    print('')
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
        if chat_to_windows_input(potential_input)!= "":
            hwnd = ctypes.windll.user32.FindWindowW(None, "mGBA - 0.10.3")
            input_to_pokemon.send_letter(hwnd, chat_to_windows_input(potential_input))

def get_window_title(hwnd):
    """Retrieve the window title for a given window handle."""
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buffer = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
        return buffer.value
    print('failed')
    return None

def get_window_class_name(hwnd):
    """Retrieve the class name of a given window handle."""
    buffer = ctypes.create_unicode_buffer(256)  # Arbitrarily large buffer
    result = ctypes.windll.user32.GetClassNameW(hwnd, buffer, 256)
    if result > 0:
        return buffer.value
    return None

def chat_to_windows_input(message):
    match message.lower():
        case "!a":
            return "VK_C"
        case "!b":
            return "VK_V"
        case "!left":
            return "VK_A"
        case "!right":
            return "VK_D"
        case "!up":
            return "VK_W"
        case "!down":
            return "VK_S"
        case "!select":
            return "VK_Z"
        case "!start":
            return "VK_X"
        case _:
            return ""



if __name__ == "__main__":
    main()


