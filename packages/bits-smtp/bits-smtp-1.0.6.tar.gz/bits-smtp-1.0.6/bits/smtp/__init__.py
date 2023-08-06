# -*- coding: utf-8 -*-
"""SMTP class file."""

import logging
import smtplib

from mailer import Mailer
from mailer import Message

class SMTP(object):
    """SMTP class."""

    def __init__(self, server, verbose=False):
        """Initialize an SMTP class instance."""
        self.server = server
        self.verbose = verbose

        # attempt to connect to SMTP server
        try:
            self.smtp = Mailer(self.server)
        except smtplib.SMTPException as e:
            print('ERROR connecting to SMTP server: %s' % (self.server))
            print(e)

    def send(self, to, frm, subject, body, attachment=None):
        """Send an email message."""
        msg = Message(From=frm, To=to)
        msg.Subject = subject
        msg.Html = body

        if attachment:
            msg.attach(attachment)

        # attempt to send the message
        try:
            self.smtp.send(msg)
            return True
        except smtplib.SMTPException as e:
            logging.error('ERROR sending email to: %s: %s', to, e)
            return False
