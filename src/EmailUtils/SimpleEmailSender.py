import smtplib as slib
from email.mime.text import MIMEText

class SimpleEmailSender:
        def __init__ (self, host, port, username, password):
            self.smtpServer = slib.SMTP_SSL(host=host, port=port)
            self.smtpServer.login(username, password)
            self.username = username
            pass
        
        def sendMessage(self, message, subject, to, user_from=None):
            msg = MIMEText(message)
            msg['Subject'] = subject
            if (user_from == None):
                msg['From'] = self.username
            else:
                msg['From'] = user_from
            msg['To'] = to
            self.smtpServer.send_message(msg)
            pass
        
        def close(self):
            self.smtpServer.close();