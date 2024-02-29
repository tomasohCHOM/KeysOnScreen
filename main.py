import threading
import tkinter as tk
import pynput

import win32gui, win32con
from time import sleep

keys = ""
NUM_VISIBLE_KEYS = 15


def test_func(text_label):
    ctrl = False

    def on_keyrelease(key):
        nonlocal ctrl
        try:
            if key == pynput.keyboard.Key.ctrl_l or key == pynput.keyboard.Key.ctrl_r:
                ctrl = False
        except Exception as e:
            pass

    def on_keypress(key):
        global keys
        nonlocal ctrl

        try:
            # Check for ctrl press
            if key == pynput.keyboard.Key.ctrl_l or key == pynput.keyboard.Key.ctrl_r:
                ctrl = True
            # Check for esc key
            elif key == pynput.keyboard.Key.esc:
                # keys += "󱊷  "
                keys += "Esc"
            # Check for enter
            elif key == pynput.keyboard.Key.enter:
                keys += "Enter"
            # Generic key press
            else:
                # TODO: Fix Nerd Font
                keys += key.char if not ctrl else ("Ctrl+c")
            # On success of reading key, update gui
            if len(keys) > NUM_VISIBLE_KEYS:
                keys = "..." + keys[len(keys) - NUM_VISIBLE_KEYS :]
            text_label.set(keys)

        except Exception as e:
            # Couldn't read a keypress, who cares
            pass

    key_listener = pynput.keyboard.Listener(
        on_press=on_keypress, on_release=on_keyrelease
    )
    key_listener.start()
    key_listener.join()


# Start a window object
root = tk.Tk()
root.title("Keystrokes")
root.geometry("800x120")

# Variable that holds the text in the window
label_text = tk.StringVar()
label_text.set("  ")


# Button to clear text on screen
def clear_text():
    global keys
    keys = ""
    label_text.set(keys)


button = tk.Button(root, text="Clear", command=clear_text)
button.pack()

# Create the label widget
label = tk.Label(
    root, textvariable=label_text, font=("JetBrainsMono Nerd Font", 30, "bold")
)
label.pack(pady=5)

# Define a thread to listen for keystrokes
listener_thread = threading.Thread(target=test_func, args=(label_text,))
listener_thread.start()


# Attempt to force the window on top of the screen
def hoist_window():
    sleep(1)
    hwnd = win32gui.FindWindow(None, "Keystrokes")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 800, 120, 0)


hoist_thread = threading.Thread(target=hoist_window)
hoist_thread.start()

# Open the window
root.mainloop()

# Resolve the listener thread incase window is closed normally
hoist_thread.join()
listener_thread.join()
