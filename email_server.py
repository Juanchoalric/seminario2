import smtplib
import time

class Email(object):

    def __init__(self, account, date):
        self.server = smtplib.SMTP('smtp.gmail.com: 587')
        time.sleep(2)
        self.password = "!Viralert123"
        self.from_addr = "viralert.sip2@gmail.com"
        self.to = account
        self.message = "El motivo de este mail es para notificarle que el dia %s usted tuvo contacto estrecho con una caso positivo de covid" %(date)

    def start_server(self):
        self.server.starttls()

    def make_login(self):
        self.server.login(self.from_addr, self.password)
        time.sleep(2)

    def send_message(self):
        self.server.sendmail(self.from_addr, self.to, self.message)

    def stop_server(self):
        self.server.quit()