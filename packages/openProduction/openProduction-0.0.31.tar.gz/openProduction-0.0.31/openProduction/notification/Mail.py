# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 16:33:09 2019

@author: Markus
"""
from openProduction.connectors.BaseConnector import ConnectorErrors
from openProduction.server import ServerInterface
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from email.header import Header
from email.utils import formataddr
import os
from email.mime.application import MIMEApplication

class Mailer:
    def __init__(self, serverIF):
        self.serverIF = serverIF
        
    @staticmethod
    def create(workDir):
        return Mailer(ServerInterface.ServerInterface.create(workDir))
    
    def sendMail(self, receiver, subject, text, html, attachment, sftp_config=None):
        if sftp_config != None:
            rv, data = self.serverIF.getSFTPConfig(sftp_config)
            if rv == ConnectorErrors.NO_ERROR:
                pass
            else:
                raise RuntimeError("error getting sftp_config %d, rv=%d"%(sftp_config, rv.value))
        else:
            rv, data = self.serverIF.listSFTPConfig(filt="type like 'MAIL'")
            if rv != ConnectorErrors.NO_ERROR:
                raise RuntimeError("error getting sftp_config, rv=%d"%(rv.value))
            if type(data) == type(None):
                raise RuntimeError("no sftp_config with type 'MAIL' found")
            data = data[0]

        if type(receiver) != type([]):
            receiver = receiver.split(",")

        sender_email = data["user"]
        password = data["password"]
        cfg = json.loads(data["config"])
        smtp_server = cfg["hostname"]
        port = cfg["port"]

        message = MIMEMultipart("html")
        message["Subject"] = subject
        message["From"] = formataddr((str(Header('openProduction', 'utf-8')), sender_email))
        message["To"] = ", ".join(receiver)
        
        # Turn these into plain/html MIMEText objects
        if text != None:
            message.attach(MIMEText(text, "plain"))
        if html != None:
            message.attach(MIMEText(html, "html"))

        if type(attachment) != type([]):
            attachment = [attachment]


        for f in attachment or []:
            with open(f, "rb") as fil:
                  message.attach(MIMEApplication(
                    fil.read(),
                    Content_Disposition='attachment; filename="%s"' % os.path.basename(f),
                    Name=os.path.basename(f)
                ))

        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            server.sendmail(
                "openProduction", receiver, message.as_string()
            )
            # TODO: Send email here
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()


if __name__ == "__main__":
    from openProduction.common import misc
    m = Mailer.create(misc.getDefaultAppFolder())


    txt = "Lieber Benutzer,\n\nder Job Bauernstolz AA (Rev. 138) an der Station Versandplatz wurde erfolgreich beendet.\n\nMit freundlichen Grüßen\nopenProduction\n\nDies ist eine automatisch generierte Email von openProduction 0.0.25"
    m.sendMail("markus.proeller@pieye.org", "Versandplatz Bauernstolz", txt, None, r"D:\work\openProduction\openProduction\notification\Mail.txt")