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
import gators.configGator as cg
import gators.databaseGator as dg
import gators.zeromqGator as zg

general = cg.config()
database = dg.config()
zeromq = zg.config()


"""
#########################STOP EDITING#####################################
***WARNING***
Don't change these following settings unless you know what you're doing!!!
##########################################################################
"""
urls = []
