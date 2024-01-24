# Import Modules
from tkinter import *
from pynput import mouse
import time
import json

# Initalize listener
listener = None
# Global variable to track whether the listener is running
listener_on = False

# File to store inputs
json_file = "inputs.json"

# List to store inputs
inputs = []

def toggle_listener():
    global listener, listener_on
    if listener_on:
        # Stop the listener
        listener.stop()
        listener_on = False
        write_to_json(inputs)
        print("Stopped")
    else:
        # Start the listener
        listener = mouse.Listener(
            on_move = on_move,
            on_click = on_click,
            on_scroll = on_scroll)
        listener.start()
        listener_on = True
        print("Started")

# Writes to .json file
def write_to_json(data):
    with open(json_file, 'w') as opened_file:
        json.dump(data, opened_file)

# Gets timestamp for input sorting
def get_time():
    return time.time()

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