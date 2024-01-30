# Import Modules
from tkinter import *
from pynput import mouse, keyboard
import time
import json

# Initalize listeners
mouse_listener = None
key_listener = None
# Global variable to track whether the listener is running
listener_on = False

# Whether the listener start should be delayed or not
delay = False

# File to store inputs
json_file = "inputs.json"

# List to store inputs
inputs = []


def without_delay():
    global delay
    delay = False
    toggle_listener()

def with_delay():
    global delay
    delay = True
    toggle_listener()

def toggle_listener():
    global mouse_listener, key_listener, listener_on
    if listener_on:
        # Stop the listener
        mouse_listener.stop()
        key_listener
        listener_on = False
        write_to_json(inputs)
        print("Stopped")
    else:
        if delay:
            time.sleep(3) # Start the listener after 3 seconds
        mouse_listener = mouse.Listener(
            on_move = on_move,
            on_click = on_click,
            on_scroll = on_scroll)
        mouse_listener.start()
        key_listener = keyboard.Listener(
            on_press = on_press,
            on_release = on_release)
        key_listener.start()
        listener_on = True
        print("Started")

# Writes to .json file
def write_to_json(data):
    with open(json_file, 'w') as opened_file:
        json.dump(data, opened_file)


# Tracks key presses
def on_press(key):
    if listener_on:
        try:
            key_str = key.char
        except AttributeError:
            if key == keyboard.Key.esc:
                toggle_listener()
            key_str = str(key)

        data = ({'time': time.time(), 
                 'type': 'key pressed',
                 'key': key_str})
        inputs.append(data)

        print('key pressed: {0}'.format(
                (key_str)))

# Tracks key releases
def on_release(key):
    if listener_on:
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        data = ({'time': time.time(), 
                 'type': 'key released',
                 'key': key_str})
        inputs.append(data)

        print('key released: {0}'.format(
                (key_str)))


# Tracks mouse movement
def on_move(x, y):
    if listener_on:
        data = ({'time': time.time(), 
                 'type': 'move',
                 'x': x,
                 'y': y})
        inputs.append(data)

        print('moved to {0}'.format(
            (x, y)))

# Tracks mouse clicks
def on_click(x, y, button, pressed):
    if listener_on:
        data = ({'time': time.time(), 
                 'type': 'pressed' if pressed else 'released',
                 'button': str(button),
                 'x': x,
                 'y': y})
        inputs.append(data)

        print('{0} {1} at {2}'.format(
            'pressed' if pressed else 'released',
            button,
            (x, y)))

# Tracks mouse scroll
def on_scroll(x, y, dx, dy):
    if listener_on:
        data = ({'time': time.time(), 
                 'type': 'scrolled',
                 'direction': 'down' if dy < 0 else 'up',
                 'x': x,
                 'y': y})
        inputs.append(data)

        print('scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))
        

# Create root window and give it a title
root = Tk()
root.title("Avery's Input Recorder")

# Add Label to display instructions
instructions_label = Label(root, text=("Press 'Toggle Listener' to start recording inputs.\n"
                                       "Alternatively, press 'Toggle Listener (w/ delay)' to start recording inputs after a 3 second delay so you can get set up.\n"
                                       "Press either button again or push the 'Esc' key to stop recording inputs\n"),
                                        font=("Helvetica", 12))
instructions_label.pack(pady=10)

# Create buttons in window to start / stop mouse listener
btn_toggle = Button(root, text="Toggle Listener", command=without_delay)
btn_toggle.pack(pady=10)

btn_toggle_delay = Button(root, text="Toggle Listener (w/ delay)", command=with_delay)
btn_toggle_delay.pack(pady=10)
 
# Execute Tkinter
root.mainloop()