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
                try:
                    matched = url.regex.match(env["REQUEST_URI"][len(c.fcgiBase):].split("?")[0])
                except:
                    matched = url.regex.match(env["PATH_INFO"])
                if matched:
                        if c.debug:
                                logURL(env, url)
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

                        newHTTPObject = url.pageObject(env, members, sessionID)

                        if env["REQUEST_METHOD"] == "GET":
                                newHTTPObject.session.history = env["REQUEST_URI"] if env.has_key("REQUEST_URL") else env["PATH_INFO"]

                        data, reply = queue.Queue(), queue.Queue()
                        dataThread = gevent.spawn(newHTTPObject.build, data, reply)
                        dataThread.join()

                        content = data.get()

                        replyData = reply.get()
                        cookieHeader = ("Set-Cookie", cookie.output(header=""))
                        header = replyData[1]
                        header.append(cookieHeader)

                        status = replyData[0]
                        header.append(("Content-Length", str(len(content))))

                        start_response(status, header)

#                        newHTTPObject.session.save()

                        del(newHTTPObject)

                        return [str(content)]

        if c.debug: log404(env)
        status = "404 NOT FOUND"
        content = "<html><body><b>404 Not Found</b></body></html>"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(content)))]
        start_response(status, headers)
        return [content]

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
