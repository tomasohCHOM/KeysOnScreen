import threading
import tkinter as tk
import pynput

keys = ""


def test_func(text_label):
    def on_keypress(key):
        global keys
        try:
            keys += key.char
            text_label.set(keys)
        except AttributeError:
            "non-key pressed"

    key_listener = pynput.keyboard.Listener(on_press=on_keypress)
    key_listener.start()


# Start a window object
root = tk.Tk()
root.title("Keystrokes")
root.geometry("800x120")

# Variable that holds the text in the window
label_text = tk.StringVar()
label_text.set("Hi this is text")


# Button to clear text on screen
def clear_text():
    label_text.set("")
    keys = ""


button = tk.Button(root, text="Clear", command=clear_text)
button.pack()

# Create the label widget
label = tk.Label(root, textvariable=label_text, font=("Arial", 30, "bold"))
label.pack(pady=5)

# Define a thread to listen for keystrokes
listener_thread = threading.Thread(target=test_func, args=(label_text,))
listener_thread.start()

# Open the window
root.mainloop()

# Resolve the listener thread incase window is closed normally
listener_thread.join()
