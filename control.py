# Import Modules
from tkinter import *
from pynput.mouse import Controller, Button
import time
import json

# File containing inputs
json_file = "inputs.json"

def string_to_button(str):
    if str == 'Button.left':
        return Button.left
    elif str == 'Button.right':
        return Button.right
    elif str == 'Button.middle':
        return Button.middle
    else:
        return Button.unknown

def replay_inputs(inputs):
    mouse = Controller()

    for i, data in enumerate(inputs):
        type = data['type']
        x = data['x']
        y = data['y']
        timestamp = data['time']

        if type == 'move':
            mouse.position = (x, y)
            print('moving to ({0}, {1})'.format(x, y))
        elif 'pressed' in type:
            button = string_to_button(type.split()[1])
            mouse.press(button)
            print('{0} at ({1}, {2})'.format(type, x, y))
        elif 'released' in type:
            button = string_to_button(type.split()[1])
            mouse.release(button)
            print('{0} at ({1}, {2})'.format(type, x, y))
        elif 'scrolled' in type:
            direction = 'down' if 'down' in type else 'up'
            mouse.scroll(0, -1) if direction == 'down' else mouse.scroll(0, 1)
            print('Scrolling {0} at ({1}, {2})'.format(direction, x, y))

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

# Replay inputs
if stored_inputs:
    replay_inputs(stored_inputs)