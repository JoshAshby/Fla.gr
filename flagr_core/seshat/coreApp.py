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
import config.config as c

import gevent
from gevent import queue

import logging
logger = logging.getLogger(c.logName+".seshat.coreApp")

import string
import random
import Cookie
import re
import urllib
import traceback

import controllers.errorController as errorController

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
        try:
            cookie.load(env["HTTP_COOKIE"])
            sessionCookie = { value.key: value.value for key, value in cookie.iteritems() }
            sessionID = sessionCookie["flagr_sid"]
        except:
            sessionID = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
            sessionCookie = {"flagr_sid": sessionID}


        members = {}

        newHTTPObject = None

        for url in c.urls:
            try:
                matched = url.regex.match(env["REQUEST_URI"][len(c.fcgiBase):].split("?")[0])
            except:
                matched = url.regex.match(env["PATH_INFO"])
            if matched:
                matchedItems = matched.groups()
                for item in range(len(matchedItems)):
                    try:
                        bits = matchedItems[item].strip("/")
                        if len(bits.split("/")) > 1:
                            members.update({item: bits.split("/")})
                        else:
                            members.update({item: bits})
                    except:
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

                newHTTPObject = url.pageObject(env, members, sessionID)
                if c.debug:
                        logURL(env, url)
                break

        if not newHTTPObject:
            newHTTPObject = errorController.error404(env, members, sessionID)
            if c.debug: log404(env)


        if env["REQUEST_METHOD"] == "GET":
                newHTTPObject.session.history = env["REQUEST_URI"] if env.has_key("REQUEST_URL") else env["PATH_INFO"]

        data, reply = queue.Queue(), queue.Queue()
        dataThread = gevent.spawn(newHTTPObject.build, data, reply)
        dataThread.join()
        try:
            dataThread.get()
        except:
            members["error"] = data.get() + traceback.format_exc()
            data = queue.Queue()
            newHTTPObject = errorController.error500(env, members, sessionID)
            dataThread = gevent.spawn(newHTTPObject.build, data, reply)
            dataThread.join()

        content = data.get()
        replyData = reply.get()

        header = replyData[1]
        status = replyData[0]

        #Hack to see if this works...
        if status == "404 NOT FOUND":
            newHTTPObject = errorController.error404(env, members, sessionID)
            if c.debug: log404(env)

            if env["REQUEST_METHOD"] == "GET":
                    newHTTPObject.session.history = env["REQUEST_URI"] if env.has_key("REQUEST_URL") else env["PATH_INFO"]

            data, reply = queue.Queue(), queue.Queue()
            dataThread = gevent.spawn(newHTTPObject.build, data, reply)
            dataThread.join()

            content = data.get()

            replyData = reply.get()
            header = replyData[1]
            status = replyData[0]

        if content:
            for morsal in sessionCookie:
                cookieHeader = ("Set-Cookie", ("%s=%s")%(morsal, sessionCookie[morsal]))
                header.append(cookieHeader)
            header.append(("Content-Length", str(len(content))))

        start_response(status, header)

        del(newHTTPObject)

        if content:
            return [str(content)]
        else:
            return []


def logURL(env, url):
    uri = env["REQUEST_URI"] if env.has_key("REQUEST_URI") else env["PATH_INFO"]
    remote = env["REMOTE_ADDR"] if env.has_key("REMOTE_ADDR") else (env["HTTP_HOST"] if env.has_key("HTTP_HOST") else "locahost")
    logger.debug("""\n\r----------------------------
    Method: %s
    URL: %s
    Object: %s
    IP: %s
""" % (env["REQUEST_METHOD"], uri, url.pageObject.__module__+"."+url.pageObject.__name__, remote))


def log404(env):
    uri = env["REQUEST_URI"] if env.has_key("REQUEST_URI") else env["PATH_INFO"]
    remote = env["REMOTE_ADDR"] if env.has_key("REMOTE_ADDR") else (env["HTTP_HOST"] if env.has_key("HTTP_HOST") else "locahost")

    logger.warn("""\n\r-------404 NOT FOUND--------
    Method: %s
    URL: %s
    IP: %s
    """ % (env["REQUEST_METHOD"], uri, remote))
