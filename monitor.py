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

# Set to store currently pressed keys
pressed_keys = set()

# File to store inputs
json_file = "inputs.json"

# List to store inputs
inputs = []

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
        # Start the listener
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

# Gets timestamp for input sorting
def get_time():
    return time.time()

# Tracks key presses
def on_press(key):
        key_str = str(key).replace("Key.", "").replace("'", "")

        # Check if key is not already in "pressed" state
        if key_str not in pressed_keys:
            data = ({'time': get_time(), 
                    'type': 'key pressed ' + key_str,
                    'x': '',
                    'y': ''})
            inputs.append(data)
            pressed_keys.add(key_str)
            print('key pressed: {0}'.format(
                    (key_str)))

# Tracks key releases
def on_release(key):
    if listener_on:
        key_str = str(key).replace("Key.", "").replace("'", "")

        data = ({'time': get_time(), 
                 'type': 'key release ' + key_str,
                 'x': '',
                 'y': ''})
        inputs.append(data)
        pressed_keys.discard(key_str)
        print('key released: {0}'.format(
                (key_str)))


# Tracks mouse movement
def on_move(x, y):
    if listener_on:
        data = ({'time': get_time(), 
                 'type': 'move',
                 'x': x,
                 'y': y})
        inputs.append(data)
        print('moved to {0}'.format(
            (x, y)))

# Tracks mouse clicks
def on_click(x, y, button, pressed):
    if listener_on:
        action = '{0} {1}'.format(
            'pressed' if pressed else 'released',
            button)
        data = ({'time': get_time(), 
                 'type': action,
                 'x': x,
                 'y': y})
        inputs.append(data)
        print(action)

# Tracks mouse scroll
def on_scroll(x, y, dx, dy):
    if listener_on:
        uppies = 'down' if dy < 0 else 'up'
        data = ({'time': get_time(), 
                 'type': 'scrolled' + uppies,
                  'x': x,
                  'y': y})
        inputs.append(data)
        print('scrolled {0} at {1}'.format(
            uppies,
            (x, y)))
        

# Create root window and give it a title
root = Tk()
root.title("Avery's Input Recorder & Repeater")

# Create button in window to start / stop mouse listener
btn_toggle_listener = Button(root, text="Toggle Listener", command=toggle_listener)
btn_toggle_listener.pack(pady=10)
 
# Execute Tkinter
root.mainloop()