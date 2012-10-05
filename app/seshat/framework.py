#!/usr/bin/env python2
"""
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

import signal

from gevent import queue
import string
import random
import Cookie
import re
import urllib

import models.basic.sessionModel as sm

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
                        if c.debug: print"\n\r----------------------------\n\r", env["REQUEST_METHOD"], env["REQUEST_URI"]

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
                        c.session.history = env["REQUEST_URI"]

                        newHTTPObject = url.pageObject(env, members)

                        data, reply = queue.Queue(), queue.Queue()
                        dataThread = gevent.spawn(newHTTPObject.build, data, reply)
                        dataThread.join()

                        replyData = reply.get()
                        cookieHeader = ("Set-Cookie", cookie.output(header=""))
                        header = replyData[1]
                        header.append(cookieHeader)

                        status = replyData[0]

                        c.session.commit()

                        start_response(status, header)

                        return data

        status = "404 NOT FOUND"
        headers = []
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

        print ("Now serving py as a fastcgi server at %s:%i" % (address, port))
        print "Press Ctrl+c or send SIGQUIT to stop"

        print "\r\n\r\nNo logging of requests done here."
        print "Check your server logs instead."
        return server


def forever():
        """
        Server

        Starts the server
        """
        gevent.signal(signal.SIGQUIT, gevent.shutdown)
        server = main()
        try:
                server.serve_forever()
        except KeyboardInterrupt:
                gevent.shutdown
