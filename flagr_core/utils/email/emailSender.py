#!/usr/bin/env python
"""
Base util for sending emails from within fla.gr

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pystache

import utils.markdownUtils as mdu
import models.template.templateModel as tm
import config.dbBase as db
import config.config as c

from gevent import monkey; monkey.patch_all()
import gevent

from gevent_zeromq import zmq
context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.connect("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "sendEmail")

import json

import logging
logger = logging.getLogger(c.logName+"email.sender")

s = None

class emailer(object):
    def __init__(self):
        self.error = False
        if c.siteConfig.has_key("emailServerNotLocalhost"):
            logger.debug("Email server not localhost, attempting to login")
            self.s = smtplib.SMTP(c.siteConfig["emailServerHost"], int(c.siteConfig["emailServerPort"]))
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            try:
                self.s.login(c.siteConfig["emailServerLoginEmail"], c.siteConfig["emailServerLoginPassword"])
            except Exception as exc:
                self.error = True
                logger.critical("Could not login to email server!")
                logger.debug(exc)
        else:
            try:
                self.s = smtplib.SMTP('localhost')
            except Exception as exc:
                self.error = True
                logger.critical("Could not connect to localhost email server!")
                logger.debug(exc)
        logger.debug("Connected to email server...")


    def sendMessage(self, tmplid, tmplData, whoTo, subject):
        """
        Finds the given template id in the database, renders it into HTML
        via markdown, then runs mustache to fill in template data. Finally,
        the rendered and compiled template is put into an email package
        and sent via email to the person given by `whoTo`

        :param tmplid: The document id of the template for which to use for the email
        :param tmplData: The data which should be placed into the template with mustache
        :param whoTo: The email address of the person who this email should go to
        :param subject: The subject of the email
        :return:
        """
        error = False
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To'] = whoTo
        msg['From'] = "fla.gr"

        tmplObj = tm.templateORM.load(db.couchServer, tmplid)
        tmpl = tmplObj.template

        tmplMarked = mdu.mark(tmpl)

        compiledTmpl = pystache.render(tmplMarked, tmplData)

        tmplText = pystache.render(tmpl, tmplData)

        part1 = MIMEText(tmplText, 'plain')
        part2 = MIMEText(compiledTmpl, 'html')

        msg.attach(part1)
        msg.attach(part2)

        if not error:
            logger.debug("Sending message...")
            self.s.sendmail("fla.gr", [whoTo], msg.as_string())
            return True
        else:
            raise Exception("Could not send email, see logs for detail.")


    def sendMessages(self, tmplid, tmplData, whoTo, subject):
        """
        Same as above however sends the message to multiple people
        Finds the given template id in the database, renders it into HTML
        via markdown, then runs mustache to fill in template data. Finally,
        the rendered and compiled template is put into an email package
        and sent via email to the person given by `whoTo`

        :param tmplid: The document id of the template for which to use for the email
        :param tmplData: The data which should be placed into the template with mustache
            Should be in a dict whos keys are the emails in `whoTo` and the values are the
            data
        :param whoTo: The email address of the person who this email should go to
            should be a list
        :param subject: The subject of the email
        :return:
        """
        error = False
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To'] = whoTo
        msg['From'] = "fla.gr"

        tmplObj = tm.templateORM.load(db.couchServer, tmplid)
        tmpl = tmplObj.template

        tmplMarked = mdu.mark(tmpl)

        for person in whoTo:
            compiledTmpl = pystache.render(tmplMarked, tmplData[person])

            tmplText = pystache.render(tmpl, tmplData[person])

            part1 = MIMEText(tmplText, 'plain')
            part2 = MIMEText(compiledTmpl, 'html')

            msg.attach(part1)
            msg.attach(part2)

            if not error:
                logger.debug("Sending message...")
                self.s.sendmail("fla.gr", [person], msg.as_string())
                return True
            else:
                raise Exception("Could not send email, see logs for detail.")


    def getMessages(self):
        while True:
            reply = zmqSock.recv()
            jsonBit = reply.split(":", 1)[1]
            logger.debug("Got: "+jsonBit)

            data = json.loads(jsonBit)

            if type(data["whoTo"]) != list:
                logger.debug("Sending single message...")
                self.sendMessage(data["tmplID"], data["tmplData"], data["whoTo"], data["subject"])
            else:
                logger.debug("Sending same tmpl to multiple people...")
                self.sendMessages(data["tmplID"], data["tmplData"], data["whoTo"], data["subject"])


def start():
    logger.debug("Starting up email sending service...")
    sender = emailer()
    ser = gevent.spawn(sender.getMessages)
    try:
        ser.join()
    except Exception as exc:
        sender.s.quit()
        logger.debug("emailSender: Got exception: " + exc)
        gevent.shutdown
    except KeyboardInterrupt:
        sender.s.quit()
        gevent.shutdown
    else:
        sender.s.quit()
        gevent.shutdown
