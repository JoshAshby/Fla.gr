#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
import gevent

from gevent_zeromq import zmq
context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.connect("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "indexUpdate")

from whoosh.index import create_in
from whoosh.fields import *

import os

import models.flag.flagModel as fm
import config.dbBase as db

import config.config as c

import logging
logger = logging.getLogger(c.logName+".search")


flagSchema = Schema(title=TEXT,
    id=ID(stored=True, unique=True),
    description=TEXT,
    labels=KEYWORD(commas=True),
    url=TEXT,
    created=DATETIME,
    userID=TEXT)

flagSearchIndex = "/.flagSearchIndex"

if not os.path.exists(c.baseFolder+flagSearchIndex):
    os.mkdir(c.baseFolder+flagSearchIndex)
    logger.debug("Made directory: "+c.baseFolder+flagSearchIndex)


def buildIndexes():
    logger.debug("Making new index of flags...")
    ix = create_in(c.baseFolder+flagSearchIndex, flagSchema)

    writer = ix.writer()

    flags = list(fm.flagORM.view(db.couchServer, 'typeViews/flag'))
    flags = fm.formatFlags(flags, True)

    for flag in flags:
        logger.debug("Flag: " +flag.id+" Indexed")
        labels = ", ".join(flag.labels)

        writer.update_document(title=flag.title,
            id=flag.id,
            description=flag.description,
            labels=labels,
            url=flag.url,
            userID=flag.userID,
            created=flag.created)

    writer.commit()


def updateFlags():
    logger.debug("Rebuilding index of flags...")
    ix = open(c.baseFolder+flagSearchIndex)

    flags = list(fm.flagORM.view(db.couchServer, 'typeViews/flag'))
    flags = fm.formatFlags(flags, True)

    currentFlags = set()
    indexedFlags = set()

    with ix.searcher() as searcher:
        writer = ix.writer()

        for fields in searcher.all_stored_fields():
            if fields["id"] not in currentFlags:
                writer.delete_by_term('id', fields["id"])
            else:
                indexedFlags.add(fields["id"])

    for flag in flags:
        labels = ", ".join(flag.labels)

        writer.update_document(title=flag.title,
            id=unicode(flag.id),
            description=flag.description,
            labels=labels,
            url=flag.url,
            userID=flag.userID,
            created=flag.created)
        currentFlags.add(flag.id)

    writer.commit()


def updateIndex():
    count = 0
    while True:
        reply = zmqSock.recv()
        logger.debug("Got: "+reply)
        if reply == "flagIndexUpdate up":
            logger.debug("Got count, count is currently: "+count)
            count += 1
            if count >= 5:
                update()
                count = 0

            elif reply == "flagIndexUpdate now":
                logger.debug("Got manual, updating index.")
                update()
                count = 0
        logger.debug("Count is now: "+count)


def start():
    ser = gevent.spawn(updateIndex)
    try:
        ser.join()
    except Exception as exc:
        gevent.shutdown
    except KeyboardInterrupt:
        gevent.shutdown
    else:
        gevent.shutdown
