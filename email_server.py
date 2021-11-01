import smtplib
import time
from email.message import EmailMessage

class Email(object):

    def __init__(self, account, date):
        self.server = smtplib.SMTP('smtp.gmail.com: 587')
        time.sleep(2)
        self.password = "!Viralert123"
        self.from_addr = "viralert.sip2@gmail.com"
        self.to = account
        self.SUBJECT = "Alerta de contacto estrecho"
       
    def start_server(self):
        self.server.starttls()

    def make_login(self):
        self.server.login(self.from_addr, self.password)
        time.sleep(2)

    def send_message(self):
        message = EmailMessage()
        message['Subject'] = self.SUBJECT
        message['From'] = self.from_addr 
        message['To'] = self.to
        textito = open("viralertMail.html")
        message.set_content(textito.read(), subtype='html')
        self.server.send_message(message)

    def stop_server(self):
        self.server.quit()