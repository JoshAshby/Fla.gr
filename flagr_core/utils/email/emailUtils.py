#!/usr/bin/env python
"""
fla.gr aid for talking with the email daemon
"""
import config.config as c
import config.zmqBase as zmqc

import json

import logging
logger = logging.getLogger(c.logName+".emailUtils")


def sendMessage(tmplID, tmplData, whoTo, subject):
    """
    Finds the given template id in the database, renders it into HTML
    via markdown, then runs mustache to fill in template data. Finally,
    the rendered and compiled template is put into an email package
    and sent via email to the person given by `whoTo`

    :param tmplID: The document id of the template for which to use for the email
    :param tmplData: The data which should be placed into the template with mustache
    :param whoTo: The email address of the person who this email should go to
    :param subject: The subject of the email
    :return:
    """
    dictToSend = {"tmplID": tmplID, "tmplData": tmplData, "whoTo": whoTo, "subject":subject}

    msg = "sendEmail:" + json.dumps(dictToSend)

    logger.debug("Sending signal: %s" % msg)
    zmqc.zmqSock.send(msg)
    logger.debug("Signal sent")

