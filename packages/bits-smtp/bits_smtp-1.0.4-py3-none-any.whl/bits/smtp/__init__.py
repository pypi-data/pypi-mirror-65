# -*- coding: utf-8 -*-
"""SMTP class file."""

import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

class SMTP(object):
    """SMTP class."""

    def __init__(self, server, verbose=False):
        """Initialize an SMTP class instance."""
        self.server = server
        self.verbose = verbose

        # smtplib package
        self.smtplib = smtplib

        # attempt to connect to SMTP server
        try:
            self.smtp = smtplib.SMTP(self.server)
        except smtplib.SMTPException as e:
            print('ERROR connecting to SMTP server: %s' % (self.server))
            print(e)

    def send(self, to, frm, subject, body, attachment=None):
        """Send an email message."""
        # create the message string
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = frm
        msg['To'] = to
        msg.set_content(body)

        if attachment:
            with open(attachment, 'rb') as fp:
                data = fp.read()
                ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=attachment)

        # attempt to send the message
        try:
            self.smtp.send_message(msg)
            print(f"Email Successfully sent to: {to}")
        except smtplib.SMTPException as e:
            print(f'ERROR sending email to: {to}')
            print(e)
