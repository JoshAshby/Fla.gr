#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c

import gevent

import logging
logger = logging.getLogger(c.general.logName+".seshat.dispatch")

from seshat.requestItem import requestItem
import controllers.error as error


def dispatch(env, start_response):
    """
    WSGI dispatcher

    Start off by making the global request object that gets passed around from
    this dispatcher to the controllers to the templater, the request object
    contains all the base logic to pull out the URL request parameters, build
    the session and gather the configuration bucket. It also contains logic for
    building the final header that is returned to the browser when a request is
    finished.

    After this request object has been initialized, we then go through and try
    to find a match in the global urls dictionary which contains key values of
    the regex as the key and the object to route a match on that regex to as
    the value. From there it's either processing and returning the data from
    that controller object or it's returning a 404 or 500 error page.

    """
    request = requestItem(env)
    newHTTPObject = None


    """
    This needs to be rewritten to automatically pull out the URL since the URL scheme
    is settled upon with /blah/blah/id the use of regex and matching a regex is
    old slower and partially redudant with the autorouter
    """
    for url in c.urls:
        try:
            matched = url.regex.match(env["REQUEST_URI"][len(c.general.fcgiBase):].split("?")[0])
        except:
            matched = url.regex.match(env["PATH_INFO"])

        if matched:
            matchedItems = matched.groups()
            request.id = matchedItems

            newHTTPObject = url.pageObject(request)
            if c.general.debug: logURL(env, url)

            break

    try:
        if not newHTTPObject:
            return error404(request, start_response)

        dataThread = gevent.spawn(newHTTPObject.build)
        dataThread.join()
        try:
            content, replyData = dataThread.get()
        except Exception as e:
            request.error = e.message
            return error500(request, start_response)

        header = replyData[1]
        status = replyData[0]

        #Hack to see if this works...
        if status == "404 NOT FOUND":
            return error404(request, start_response)

        if content:
            header = request.buildHeader(header, len(content))

        start_response(status, header)

        del(newHTTPObject)

        if content:
            return [str(content)]
        else:
            return []

    except Exception as e:
        request.error = e
        return error500(request, start_response)


def error404(request, start_response):
    """
    Returns a base 404 not found error page
    """
    newHTTPObject = error.error404(request)
    if c.general.debug: log404(request)

    dataThread = gevent.spawn(newHTTPObject.build)
    dataThread.join()

    content, replyData = dataThread.get()

    header = replyData[1]
    status = replyData[0]

    header = request.buildHeader(header, len(content))

    start_response(status, header)

    del(newHTTPObject)

    return [str(content)]


def error500(request, start_response):
    """
    Returns the base 500 errorpage with the optional error message in the page.
    These errors are logged in a special error log and there is also a general
    error logged to the default logger.
    """
    newHTTPObject = error.error500(request)
    if c.general.debug: log500(request)

    dataThread = gevent.spawn(newHTTPObject.build)
    dataThread.join()

    content, replyData = dataThread.get()

    header = replyData[1]
    status = replyData[0]

    header = request.buildHeader(header, len(content))

    start_response(status, header)

    del(newHTTPObject)

    return [str(content)]


def logURL(env, url):
    uri = env["REQUEST_URI"] if env.has_key("REQUEST_URI") else env["PATH_INFO"]
    remote = env["REMOTE_ADDR"] if env.has_key("REMOTE_ADDR") else (env["HTTP_HOST"] if env.has_key("HTTP_HOST") else "localhost")
    logger.debug("""\n\r----------------------------
    Method: %s
    URL: %s
    Object: %s
    IP: %s
""" % (env["REQUEST_METHOD"], uri, url.pageObject.__module__+"."+url.pageObject.__name__, remote))


def log500(request):
    env = request._env
    uri = env["REQUEST_URI"] if env.has_key("REQUEST_URI") else env["PATH_INFO"]
    remote = env["REMOTE_ADDR"] if env.has_key("REMOTE_ADDR") else (env["HTTP_HOST"] if env.has_key("HTTP_HOST") else "localhost")
    logger.error("""\n\r-------500 INTERNAL SERVER ERROR --------
    Method: %s
    URL: %s
    IP: %s
    ERROR: %s
    """ % (env["REQUEST_METHOD"], uri, remote, request.error))


def log404(request):
    env = request._env
    uri = env["REQUEST_URI"] if env.has_key("REQUEST_URI") else env["PATH_INFO"]
    remote = env["REMOTE_ADDR"] if env.has_key("REMOTE_ADDR") else (env["HTTP_HOST"] if env.has_key("HTTP_HOST") else "localhost")
    logger.warn("""\n\r-------404 NOT FOUND--------
    Method: %s
    URL: %s
    IP: %s
    """ % (env["REQUEST_METHOD"], uri, remote))
