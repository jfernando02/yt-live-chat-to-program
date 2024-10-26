import ctypes
from ctypes import wintypes
import time

# Load user32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Define constants
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

# Virtual Key Codes for the letters
VK_CODES = {
    "VK_A": 0x41,
    "VK_C": 0x43,
    "VK_D": 0x44,
    "VK_S": 0x53,
    "VK_V": 0x56,
    "VK_W": 0x57,
    "VK_X": 0x58,
    "VK_Z": 0x5A
}

# Function to map virtual keycode to scan code
MapVirtualKeyA = user32.MapVirtualKeyA

# Function to post messages to a window
PostMessageA = user32.PostMessageA


def send_letter(hwnd, vk_key_string):
    vk_key = VK_CODES.get(vk_key_string.upper())  # Ensure upper case for consistency
    if vk_key is None:
        raise ValueError(f"Invalid virtual key string: {vk_key_string}")

    scancode = MapVirtualKeyA(vk_key, 0)
    lparam_down = 0x00000001 | (scancode << 16)
    lparam_up = 0xC0000001 | (scancode << 16)

    print(f"Sending key '{vk_key_string}' with VK_CODE: {vk_key}, ScanCode: {scancode}")

    # Send WM_KEYDOWN
    result = PostMessageA(hwnd, WM_KEYDOWN, vk_key, lparam_down)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    time.sleep(0.1)
    # Send WM_KEYUP
    result = PostMessageA(hwnd, WM_KEYUP, vk_key, lparam_up)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())

    print(f"Sent key '{vk_key_string}' to the window (HWND: {hwnd}).")


# Example usage
def main():
    hwnd = ctypes.windll.user32.FindWindowW(None, "mGBA - 0.10.3")
    try:
        send_letter(hwnd, 'VK_C')
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()