import smtplib, ssl
from smtplib import SMTP_SSL as SMTP 
import os
import re
import sys
from email.mime.text import MIMEText
from dotenv import load_dotenv

def sendmail(receiver, message, subject):
    load_dotenv() 
    
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_USER = os.getenv('SMTP_USER')

    text_subtype = 'plain'
    port = 465

    try:
        msg = MIMEText(message, text_subtype)
        msg['Subject']= subject
        msg['From']   = SMTP_USER

        conn = SMTP(SMTP_SERVER)
        conn.set_debuglevel(False)
        conn.login(SMTP_USER, SMTP_PASSWORD)
        try:
            conn.sendmail(SMTP_USER, receiver, msg.as_string())
        finally:
            conn.quit()
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message

    return

