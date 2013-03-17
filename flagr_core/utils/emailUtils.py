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

import logging
logger = logging.getLogger(c.logName+".emailUtils")


def sendMessage(tmplid, tmplData, whoTo, subject):
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

    if c.siteConfig.has_key("emailServerNotLocalhost"):
        s = smtplib.SMTP(c.siteConfig["emailServerHost"], int(c.siteConfig["emailServerPort"]))
        s.ehlo()
        s.starttls()
        s.ehlo()
        try:
            s.login(c.siteConfig["emailServerLoginEmail"], c.siteConfig["emailServerLoginPassword"])
        except Exception as exc:
            error = True
            logger.critical("Could not login to email server!")
            logger.debug(exc)
    else:
        try:
            s = smtplib.SMTP('localhost')
        except Exception as exc:
            error = True
            logger.critical("Could not connect to localhost email server!")
            logger.debug(exc)

    if not error:
        s.sendmail("fla.gr", [whoTo], msg.as_string())
        s.quit()
        return True
    else:
        raise Exception("Could not send email, see logs for detail.")
