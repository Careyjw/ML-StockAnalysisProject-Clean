from EmailUtils.EMessage import EMessage
from EmailUtils.EClient import EClient
import smtplib as slib
from email.mime.text import MIMEText

class EMessageSender:
        def __init__ (self, host, port, username, password):
            '''Initializes the object
            :param host: Emailing Service's host name (i.e. smtp.gmail.com for gmail)
            :param port: Port to connect to the smtp server on
            :param username: Email address of the account to connect to
            :param password: Password of the account to connect to
            '''
            self.smtpServer = slib.SMTP_SSL(host=host, port=port)
            self.smtpServer.login(username, password)
            self.username = username
            pass
        
        def sendMessage(self, message : "EMessage", client : "EClient"):
            '''Sends the message to the client
            '''
            msg = MIMEText(message.body)
            msg['Subject'] = message.subject
            msg['From'] = self.username
            msg['To'] = client.clientAddress
            self.smtpServer.send_message(msg)
        
        def close(self):
            '''Closes the server connection
            '''
            self.smtpServer.close();