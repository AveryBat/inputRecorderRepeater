# Import Modules
from tkinter import *
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
from pynput.mouse import Controller as MController
from pynput.mouse import Button as MButton
from pynput.keyboard import Key, Controller as KController
import time
import json

# Global variable to track whether the recording should start after a delay
delay = False
# Global variable to track how many times the repeater should loop
loops = 1

# List to store inputs
inputs = []
# File to read inputs from
json_file = "inputs.json"


# Converts 'special' key strings into their respective keys
special_keys = {"Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

# Converts mouse button strings to Button objects
def string_to_button(str):
    if str == 'Button.left':
        return MButton.left
    elif str == 'Button.right':
        return MButton.right
    elif str == 'Button.middle':
        return MButton.middle
    else:
        return MButton.unknown


# Change .json file being read from
def json_read():
    global json_file, inputs
    new_json_file = simpledialog.askstring("Input", "Enter the name of the .json file you wish to read from:")
    if new_json_file:
        if not new_json_file.endswith(".json"):
            new_json_file += ".json"
        json_file = new_json_file
        inputs = read_from_json(json_file)
        update_label()
        print(f"Changed .json file to: {json_file}")

# Reads from .json file
def read_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File '(file_path)' not found")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding .json in file '(file_path)'")
        return None
    
# Stores information from .json file in a list
inputs = read_from_json(json_file)


def change_loop():
    global loops
    new_loops = simpledialog.askstring("Input", "Enter the number of times you wish the inputs to repeat:")
    if new_loops:
        try:
            new_loops = int(new_loops)
            # Ensure the value is at least 1
            if new_loops < 1:
                raise ValueError("Invalid input. Please enter a positive integer.")
        except ValueError as e:
            new_loops = 1
            messagebox.showerror("Invalid Input", str(e))
            print(f"Invalid input. Setting number of loops to 1. ({e})")
            
        loops = new_loops
        update_label()
        print(f"Changed # of loops to: {loops}")


# Replay inputs
def without_delay():
    global delay
    delay = False
    replay_inputs()

# Replay inputs with a delay
def with_delay():
    global delay
    delay = True
    replay_inputs()

# Replays the inputs
def replay_inputs():
    global loops, inputs
    # Tracks how many loops have been gone through
    repeats = 0
    # Stores information from .json file in a list
    inputs = read_from_json(json_file)
    # Controllers
    mouse = MController()
    keyboard = KController()

    if delay:
            time.sleep(3) # Start the repeater after 3 seconds

    while loops > 0:
        # Goes through all the inputs in order
        for i, data in enumerate(inputs):
            type = data['type']
            timestamp = data['time']

            # If keyboard
            if type == "key pressed" or type == "key released":
                key = data['key'] if 'Key.' not in data['key'] else special_keys[data['key']]

                if type == "key pressed":
                    keyboard.press(key)
                    print('key pressed: {0}'.format(key))
                else:
                    keyboard.release(key)
                    print('key released: {0}'.format(key))
            
            # If mouse
            else:
                x = data['x']
                y = data['y']

                if type == "pressed" or type == "released":
                    button = string_to_button(data['button'])

                    if type == "pressed":
                        mouse.press(button)
                        print('{0} at ({1}, {2})'.format(type, x, y))
                    else:
                        mouse.release(button)
                        print('{0} at ({1}, {2})'.format(type, x, y))

                elif type == "move":
                    mouse.position = (x, y)
                    print('moving to ({0}, {1})'.format(x, y))
            
                elif type == "scrolled":
                    horizontal, vertical = data['horizontal'], data['vertical']
                    mouse.scroll(horizontal, vertical)
                    print('scrolling {0} and {1} at {2}'.format('left' if horizontal < 0 else 'right','down' if vertical < 0 else 'up', (x, y)))

            if i < len(inputs) - 1:
                # Calculate time difference between next and current event
                time_difference = inputs[i + 1]['time'] - timestamp
                time.sleep(time_difference)
        repeats = repeats + 1
        print(f"Inputs played back {repeats} time(s)")
        loops = loops - 1
    repeats = 0
    loops = 1
    update_label()


# Updates label whenever file or loops are changed
def update_label():
    instructions_label.config(text=("Press 'Start Repeater' to start recording inputs.\n\n"
                                    "Alternatively, press 'Start Repeater (w/ delay)' to start recording inputs after a 3-second delay so you can get set up.\n\n"
                                    "There is no way to end the playback early. Make sure you know what you are doing!\n\n"
                                    "You can also change which .json file is read from, and change how many times the program repeats.\n\n"
                                    f"Currently reading from {json_file} and looping {loops} times"))

# Create root window and give it a title
root = Tk()
root.title("Avery's Input Repeater")

# Add label to display instructions
instructions_label = Label(root, text=("Press 'Start Repeater' to start recording inputs.\n\n"
                                       "Alternatively, press 'Start Repeater (w/ delay)' to start recording inputs after a 3 second delay so you can get set up.\n\n"
                                       "There is no way to end the playback early. Make sure you know what you are doing!\n\n"
                                       "You can also change which .json file is read from, and change how many times the program repeats.\n\n"
                                      f"Currently reading from {json_file} and looping {loops} times"),
                                        font=("Helvetica", 12))
instructions_label.pack(pady=10)

# Button to start repeat
btn_without_delay = Button(root, text="Start Repeater", command=without_delay)
btn_without_delay.pack(pady=10)

# Button to start repeater with a delay
btn_with_delay = Button(root, text="Start Repeater (w/ delay)", command=with_delay)
btn_with_delay.pack(pady=10)

# Button to change .json file being read from
btn_json_read = Button(root, text="Change which file is being read from", command=json_read)
btn_json_read.pack(pady=10)

# Button to change how many times the inputs repeat
btn_change_loop = Button(root, text="Change how many time the recording repeats itself", command=change_loop)
btn_change_loop.pack(pady=10)
 
# Execute Tkinter
root.mainloop()