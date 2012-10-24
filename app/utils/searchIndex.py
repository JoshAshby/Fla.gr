#!/usr/bin/env python2
from gevent import monkey; monkey.patch_all()
import gevent
from gevent_zeromq import zmq
context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.connect("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "")

import logging
logger = logging.getLogger("flagrUtil.searchUpdate")

from whoosh.index import create_in
from whoosh.fields import *
import redis
import os
import flagr.models.flagModel as fm
import config as c

r = redis.Redis(db=2)

schema = Schema(title=TEXT,
                id=ID(stored=True, unique=True),
                description=TEXT,
                labels=KEYWORD,
                url=TEXT,
                author=TEXT,
                time=TEXT,
                userID=TEXT)

if not os.path.exists(c.path+"/.searchIndex"):
        os.mkdir(c.path+"/.searchIndex")

def update():
        ix = create_in(c.path+"/.searchIndex", schema)
        writer = ix.writer()

        logger.debug("Writer init...")

        for key in r.keys("flag:*:id"):
                flag = fm.flag(key.strip(":id"))
                labels = ""
                for label in flag["labels"]:
                        labels += "%s ,"%label

                labels = labels.strip(", ")

                url = u""

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                if name in ["url"]:
                                        url = flag["url"]

                writer.add_document(title=flag["title"],
                                id=unicode(flag.id),
                                description=flag["description"],
                                labels=labels,
                                url=url,
                                author=flag["author"],
                                userID=unicode(flag["userID"]),
                                time=flag["time"])

        writer.commit()
        logger.debug("Index updated, resetting count")

def updateIndex():
        count = 0
        logger.debug("Entered update context, count = 0")
        while True:
                logger.debug("Waiting for signal...")
                reply = zmqSock.recv()
                if reply:
                        logger.debug("Got signal to update, increasing count...")
                        count += 1
                        logger.debug("Count is now %i" % count)
                if count >= 5:
                        logger.debug("Count at 5 or above, updating index...")
                        update()
                        count = 0
                        logger.debug("Index updated, count reset")


def start():
        logger.debug("Spawning greenlet for updater...")
        ser = gevent.spawn(updateIndex)
        try:
                ser.join()
                logger.warn("Shutdown updater operations.")
        except Exception as exc:
                logger.critical("""Shutdown updater operations, here's why: %s""" % exc)
                gevent.shutdown
        except KeyboardInterrupt:
                logger.critical("""Shutdown updater operations for a KeyboardInterrupt. Bye!""")
                gevent.shutdown
        else:
                logger.critical("""Shutdown updater operations for unknown reason, possibly a KeyboardInterrupt...""")
                gevent.shutdown
