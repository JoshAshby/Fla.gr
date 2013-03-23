#!/usr/bin/env python
"""
Seshat config for fla.gr
Config settings

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
"""
First we need to import pythons regex module.
This is used by Seshat to build the routing
table according to what you dictate as the URL
regex below
"""
import re

appName = "fla.gr"
baseFolder = '/home/josh/repos/flagr/flagr_core'

logName = appName.replace(".", "")
logFolder = baseFolder+"/logs/"
pidFolder = baseFolder+"/pid/"
stdout = baseFolder+'/logs/out'
stderr = baseFolder+'/logs/error'

"""
We need to make
sure that the routing is taken care of properly. I'll describe
this setting later when I have more time.
"""
fcgiBase = ""

"""
Next up, which address and port do we want the server to bind to
this is the same for fastcgi or standalone gevent.
"""
address = "127.0.0.1"
port = 8000

"""
Next, do you want this framework to do some extra debugging?
"""
debug = True
#use a dummy session?
dummySession = False

"""
Finally we need to define the base url for various
things such as static assets and what not.
"""
baseURL = "http://localhost"

securityLevels = ["normal", "admin"]


"""
#########################STOP EDITING#####################################
***WARNING***
Don't change these following settings unless you know what you're doing!!!
##########################################################################
"""
urls = []
authRegex = re.compile("([^_\W]*)")
