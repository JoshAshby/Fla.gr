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

import logging
logger = logging.getLogger(c.general.logName+".seshat.request")

import string
import random
import Cookie
import re
import urllib

import models.redis.session.sessionModel as sm
import models.redis.bucket.bucketModel as bm

class requestItem(object):
  def __init__(self, env):
    self._env = env
    self.getMembers()
    self.getCookie()
    self.getSession()
    self.getCfg()

    self.method = env["REQUEST_METHOD"]

  def getMembers(self):
    members = {}
    for item in self._env['QUERY_STRING'].split("&"):
        if item:
            parts = item.split("&")
            for part in parts:
                query = part.split("=")
                members.update({re.sub("\+", " ", query[0]): urllib.unquote(re.sub("\+", " ", query[1]))})

    for item in self._env['wsgi.input']:
        if item:
            parts = item.split("&")
            for part in parts:
                query = part.split("=")
                members.update({re.sub("\+", " ", query[0]): urllib.unquote(re.sub("\+", " ", query[1]))})

  def getCookie(self):
    cookie = Cookie.SimpleCookie()
    try:
        cookie.load(self._env["HTTP_COOKIE"])
        self.sessionCookie = { value.key: value.value for key, value in cookie.iteritems() }
        self.sessionID = self.sessionCookie["flagr_sid"]
    except:
        self.sessionID = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        self.sessionCookie = {"flagr_sid": self.sessionID}

  def getSession(self):
    self.session = sm.session("session:"+self.sessionID)

  def getCfg(self):
    self.cfg = bm.cfgBuckets()

  def buildHeader(self, header, length):
      for morsal in self.sessionCookie:
          cookieHeader = ("Set-Cookie", ("%s=%s")%(morsal, self.sessionCookie[morsal]))
          header.append(cookieHeader)
      header.append(("Content-Length", str(length)))
      return header



