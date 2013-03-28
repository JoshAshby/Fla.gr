#!/usr/bin/env python
"""
Seshat config for fla.gr
This file contains all the basic pieces that fla.gr and seshat
use to determine where to put things, and how to act.
"""
import re

appName = "fla.gr"
"""
App name gets used in the logs
"""

baseFolder = '/home/josh/repos/flagr/flagr_core'
"""
where is all of the python part of fla.gr located?
"""

logName = appName.replace(".", "")
logFolder = baseFolder+"/logs/"
pidFolder = baseFolder+"/pid/"
stdout = baseFolder+'/logs/out'
stderr = baseFolder+'/logs/error'

fcgiBase = ""
"""
We need to make
sure that the routing is taken care of properly. I'll describe
this setting later when I have more time.
"""

address = "127.0.0.1"
port = 8000
"""
Which address and port do we want the server to bind to
this is the same for fastcgi or standalone gevent.
"""

debug = True
"""
Do you want this framework to do some extra debugging?
"""

dummySession = False
"""
Do we want to run a dummy session? This is like `debug` and helpful for testing
"""

baseURL = "http://localhost"
"""
Finally we need to define the base url for various
things such as static assets and what not.
"""

#########################STOP EDITING#####################################
#***WARNING***
#Don't change these following settings unless you know what you're doing!!!
##########################################################################
securityLevels = ["normal", "admin"]
urls = []
authRegex = re.compile("([^_\W]*)")
