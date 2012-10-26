#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from gevent import monkey; monkey.patch_all()
import gevent
from gevent_fastcgi.server import WSGIServer
from gevent import queue

import logging
logger = logging.getLogger("seshat.seshat")

import string
import random
import Cookie
import re
import urllib
import sys

import models.basic.sessionModel as sm
import models.blocks.helpers as helpers
cookie = Cookie.SimpleCookie()


def app(env, start_response):
        """
        WSGI app and controller

        Start off by looking through the dict of url's for a matched
        regex. If one is found, then build a dict of members, which
        includes matched groups in the regex, and query strings.

        After the dict of members is built, pass it along with the
        env to the class which is paired with the matched regex url.

        Finally, call the proper method in the class, send the headers
        and start streaming data as it's available.

        If the class provides a cookie/session data, then because of the way
        this all works, at the moment data can not be streammed. As a result
        it's all added together, then returned rather than sent out in chunks.
        """
        for url in c.urls:
                matched = url.regex.match(env["REQUEST_URI"][len(c.fcgiBase):].split("?")[0])
                if matched:
                        if c.debug:
                                logger.debug("""\n\r----------------------------
        Method: %s
        URL: %s
        Object: %s
        IP: %s
""" % (env["REQUEST_METHOD"], env["REQUEST_URI"], url.pageObject.__module__+"."+url.pageObject.__name__, env["REMOTE_ADDR"]))

                        try:
                                cookie.load(env["HTTP_COOKIE"])
                        except:
                                cookie["sid"] = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

                        members = {}

                        matchedItems = matched.groups()
                        for item in range(len(matchedItems)):
                                members.update({item: matchedItems[item]})

                        for item in env['QUERY_STRING'].split("&"):
                                if item:
                                        parts = item.split("&")
                                        for part in parts:
                                                query = part.split("=")
                                                members.update({re.sub("\+", " ", query[0]): urllib.unquote(re.sub("\+", " ", query[1]))})

                        for item in env['wsgi.input']:
                                if item:
                                        parts = item.split("&")
                                        for part in parts:
                                                query = part.split("=")
                                                members.update({re.sub("\+", " ", query[0]): urllib.unquote(re.sub("\+", " ", query[1]))})

                        sessionID = cookie.output(header="")[5:]
                        c.session = sm.session(sessionID)
                        if env["REQUEST_METHOD"] == "GET":
                                c.session.history = env["REQUEST_URI"]

                        c.session.loggedIn = helpers.boolean(c.session.loggedIn)


                        pageObject = newHTTPObject = url.pageObject(env, members)

                        data, reply = queue.Queue(), queue.Queue()
#                        dataThread = gevent.spawn(newHTTPObject.build, data, reply)
#                        dataThread.join()
                        newHTTPObject.build(data, reply)

                        replyData = reply.get()
                        cookieHeader = ("Set-Cookie", cookie.output(header=""))
                        header = replyData[1]
                        header.append(cookieHeader)

                        status = replyData[0]

                        c.session.commit()

                        start_response(status, header)

                        del(pageObject)

                        return data

        status = "404 NOT FOUND"
        if c.debug: logger.warn("""\n\r-------404 NOT FOUND--------
        Method: %s
        URL: %s
        IP: %s
        """ % (env["REQUEST_METHOD"], env["REQUEST_URI"], env["REMOTE_ADDR"]))
        headers = [("Content-type", "text/html")]
        start_response(status, headers)
        return "<html><body><b>404 Not Found</b></body></html>"


def main():
        """
        Server

        Sets up the server and all that messy stuff
        """
        if c.port and type(c.port) is str:
                port = int(c.port)
        else:
                port = 8000
        if not c.address:
                address = "127.0.0.1"
        else:
                address = c.address

        server = WSGIServer((address, port), app)

        logger.info("""Now serving py as a fastcgi server at %(address)s:%(port)i
        Press Ctrl+c if running as non daemon mode, or send a stop signal
        """ % {"address": address, "port": port})

        return server


def serveForever():
        """
        Server

        Starts the server
        """
        server = main()
        try:
                server.serve_forever()
                logger.warn("Shutdown py operations.")
        except Exception as exc:
                logger.critical("""Shutdown py operations, here's why: %s""" % exc)
                gevent.shutdown
        except KeyboardInterrupt:
                logger.critical("""Shutdown py operations for a KeyboardInterrupt. Bye!""")
                gevent.shutdown
        else:
                logger.critical("""Shutdown py operations for unknown reason, possibly a KeyboardInterrupt...""")
                gevent.shutdown
