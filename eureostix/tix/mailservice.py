import smtplib, ssl
from smtplib import SMTP_SSL as SMTP 
import os
import re
import sys
from email.mime.text import MIMEText
from dotenv import load_dotenv
import imaplib
import email
import time
import schedule
from .models import Ticket, Message
import quopri

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


def decode_header(header):
    decoded = email.header.decode_header(header)
    decoded_str = ''
    for part, encoding in decoded:
        if encoding is None:
            if isinstance(part, bytes):
                part = part.decode()
            decoded_str += part
        else:
            decoded_str += quopri.decodestring(part).decode(encoding)
    return decoded_str



def checkmails():
    print("Rufe Mails ab")
    load_dotenv()

    IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    IMAP_USER = os.getenv('IMAP_USER')
    # connect to IMAP-Server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(IMAP_USER, IMAP_PASSWORD)

    # Wähle den Posteingang (Inbox) aus
    mail.select('inbox')

    # Suche nach ungelesenen E-Mails
    result, data = mail.search(None, 'UNSEEN')

    if result == 'OK':
        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])
                
                # Absenderadresse extrahieren
                absender, absender_email = email.utils.parseaddr(email_message['From'])
                absender_name = decode_header(absender)
                
                # Betreff extrahieren
                betreff_encoded = email_message['subject']
                betreff = decode_header(betreff_encoded)

                # Inhalt der Mail extrahieren
                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            inhalt = part.get_payload(decode=True).decode()
                            break
                else:
                    inhalt = email_message.get_payload(decode=True).decode()


                # print('Neue E-Mail gefunden! Betreff:', betreff + '\nVon: ' + absender + '\nInhalt: '+ inhalt)
                ticket = Ticket.objects.create(email=absender_email, problemtype="Anderes", problemdescription=inhalt, title=betreff, name=absender_name)
                ticket.save()
                

    mail.close()
    mail.logout()

def schedule_email_check():
    schedule.every(20).seconds.do(checkmails) 