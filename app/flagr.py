#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Main application file.
Run this!

For more information, see: https://github.com/JoshAshby/

**WARNING**
Make sure you look through and change things in config.py
before running this file, to be sure it runs the way you want it to

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
try:
        import config as c
except:
        import os
        import sys
        abspath = os.path.dirname(__file__)
        sys.path.append(abspath)
        os.chdir(abspath)
        import config as c

import logging
formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
        %(message)s""")

logger = logging.getLogger("flagr")

fh = logging.FileHandler("flagr.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

import signal
import daemon

def stop(signal, frame):
        sys.exit()

def start():
        import seshat.framework as fw

        from index import *

        from controllers.authController import *
        from controllers.adminController import *
        from controllers.godController import *
        from controllers.profileController import *

        #Fla.gr specific code. Makes for easy modulation of the system...
        from flagr.controllers.flagController import *
        from flagr.controllers.labelController import *
        from flagr.controllers.youController import *
        from flagr.controllers.searchController import *

if __name__ == '__main__':
        """
        Because we're not doing anything else yet, such as starting a websockets
        server or whatever, we're going to just go into forever serve mode.
        """
        if sys.argv[0] == "-d":
                with daemon.DaemonContext(signal_map={signal.SIGINT: stop,
                        signal.SIGTERM: stop,
                        signal.SIGQUIT: stop}):
                        start()
        else:
                start()
