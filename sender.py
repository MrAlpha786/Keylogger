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
            return True
        except:
            return False

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
    from os import remove

    config = PigeonConfig()
    config.debug = True
    with open(config.filepath, 'w') as demo:
        demo.write("This is a file create for testing puposes, it will be deleted automatically. Don't try to find it.")
    Pigeon(config=config).send()
    
    remove(config.filepath)