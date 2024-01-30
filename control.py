# Import Modules
from tkinter import *
from pynput.mouse import Controller as MController
from pynput.mouse import Button as MButton
from pynput.keyboard import Key, Controller as KController
import time
import json

# File containing inputs
json_file = "inputs.json"

# Whether the listener start should be delayed or not
delay = False

# Converts 'special' key strings into their respective keys
special_keys = {"Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

def without_delay():
    global delay
    delay = False
    replay_inputs(stored_inputs)

def with_delay():
    global delay
    delay = True
    replay_inputs(stored_inputs)

def string_to_button(str):
    if str == 'Button.left':
        return MButton.left
    elif str == 'Button.right':
        return MButton.right
    elif str == 'Button.middle':
        return MButton.middle
    else:
        return MButton.unknown

def replay_inputs(inputs):
    # Controllers
    mouse = MController()
    keyboard = KController()

    if delay:
            time.sleep(3) # Start the repeater after 3 seconds

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
                # Make this better later, include dx as well as dy, just clean up in general
                direction1 = "down" if 'down' in 'direction' else 'up'
                mouse.scroll(0, -1) if direction1 == 'down' else mouse.scroll(0, 1)
                print('Scrolling {0} at ({1}, {2})'.format(direction1, x, y))

        if i < len(inputs) - 1:
            # Calculate time difference between next and current event
            time_difference = inputs[i + 1]['time'] - timestamp
            time.sleep(time_difference)


def read_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File '(file_path)' not found")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '(file_path)'")
        return None
    

# Read inputs from json file
stored_inputs = read_from_json(json_file)

# Create root window and give it a title
root = Tk()
root.title("Avery's Input Repeater")

# Add Label to display instructions
instructions_label = Label(root, text=("Press 'Start Repeater' to start recording inputs.\n"
                                       "Alternatively, press 'Start Repeater (w/ delay)' to start recording inputs after a 3 second delay so you can get set up.\n"
                                       "There is no way to end the playback early. Make sure you know what you are doing!\n"),
                                        font=("Helvetica", 12))
instructions_label.pack(pady=10)

# Create buttons in window to start / stop mouse listener
btn_toggle = Button(root, text="Start Repeater", command=without_delay)
btn_toggle.pack(pady=10)

btn_toggle_delay = Button(root, text="Start Repeater (w/ delay)", command=with_delay)
btn_toggle_delay.pack(pady=10)
 
# Execute Tkinter
root.mainloop()