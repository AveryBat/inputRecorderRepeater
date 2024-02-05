# Import Modules
from tkinter import *
import tkinter.simpledialog as simpledialog
from pynput import mouse, keyboard
import time
import json


# Initalize listeners
mouse_listener = None
key_listener = None
# Global variable to track whether the listener is running
listener_on = False
# Global variable to track whether the recording should start after a delay
delay = False

# List to store inputs
inputs = []
# File to store inputs to
json_file = "inputs.json"


# Change .json file being written to
def change_name_json():
    global json_file
    new_json_file = simpledialog.askstring("Input", "Enter the name of the .json file you wish to write to:")
    if new_json_file:
        if not new_json_file.endswith(".json"):
            new_json_file += ".json"
        json_file = new_json_file
        update_label()
        print(f"Changed .json file to: {json_file}")

# Writes to .json file
def write_to_json(data):
    with open(json_file, 'w') as opened_file:
        json.dump(data, opened_file)


# Start recording without a delay
def without_delay():
    global delay
    delay = False
    toggle_listener()

# Start recording with a delay
def with_delay():
    global delay
    delay = True
    toggle_listener()

# Starts / stops tracking inputs
def toggle_listener():
    global mouse_listener, key_listener, listener_on
    if listener_on:
        # Stop the listener
        mouse_listener.stop()
        key_listener.stop()
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


# Tracks key presses
def on_press(key):
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
    data = ({'time': time.time(), 
             'type': 'move',
             'x': x,
             'y': y})
    inputs.append(data)

    print('moved to {0}'.format(
          (x, y)))

# Tracks mouse clicks
def on_click(x, y, button, pressed):
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
    data = ({'time': time.time(), 
             'type': 'scrolled',
             'horizontal': int(dx),
             'vertical': int(dy),
             'x': x,
             'y': y})
    inputs.append(data)

    print('scrolled {0} and {1} at {2}'.format(
          'left' if dx < 0 else 'right',
          'down' if dy < 0 else 'up',
          (x, y)))
        

# Updates label whenever file is changed
def update_label():
    instructions_label.config(text=("Press 'Toggle Listener' to start recording inputs.\n\n"
                                    "Alternatively, press 'Toggle Listener (w/ delay)' to start recording inputs after a 3-second delay so you can get set up.\n\n"
                                    "Press either button again or push the 'Esc' key to stop recording inputs.\n\n"
                                    "You can also change which .json file is written to in order to save multiple input recordings.\n\n"
                                   f"Currently writing to {json_file}"),
                                     font=("Helvetica", 12))

# Create root window and give it a title
root = Tk()
root.title("Avery's Input Recorder")

# Add Label to display instructions
instructions_label = Label(root, text=("Press 'Toggle Listener' to start recording inputs.\n\n"
                                       "Alternatively, press 'Toggle Listener (w/ delay)' to start recording inputs after a 3-second delay so you can get set up.\n\n"
                                       "Press either button again or push the 'Esc' key to stop recording inputs.\n\n"
                                       "You can also change which .json file is written to in order to save multiple input recordings.\n\n"
                                      f"Currently writing to {json_file}"),
                                        font=("Helvetica", 12))
instructions_label.pack(pady=10)

# Button to start recorder
btn_without_delay = Button(root, text="Toggle Listener", command=without_delay)
btn_without_delay.pack(pady=10)

# Button to start recorder with a delay
btn_with_delay = Button(root, text="Toggle Listener (w/ delay)", command=with_delay)
btn_with_delay.pack(pady=10)

# Button to change .json file being written to
btn_change_name_json = Button(root, text="Change which file is being written to", command=change_name_json)
btn_change_name_json.pack(pady=10)
 
# Execute Tkinter
root.mainloop()