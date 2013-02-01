#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main application file.
Run this!

For more information, see: https://github.com/JoshAshby/

**WARNING**
Make sure you look through and change things in config.py
before running this file, to be sure it runs the way you want it to

This is a test

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import sys
import os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import config as c

def setupLog():
        import logging
        level = logging.WARNING
        if c.debug:
                level = logging.DEBUG

        formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
        %(message)s""")

        logger = logging.getLogger(c.logName)
        logger.setLevel(level)

        fh = logging.FileHandler(c.logFolder+c.logName+".log")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        if c.debug and "noDaemon" in sys.argv:
                """
                Make sure we're not in daemon mode if we're logging to console too
                """
                try:
                        ch = logging.StreamHandler()
                        ch.setLevel(level)
                        ch.setFormatter(formatter)
                        logger.addHandler(ch)
                except:
                        pass

        return logger

from simpleDaemon import Daemon
class app(Daemon):
        down = False
        def run(self):
                logger = setupLog()
                import seshat.framework as fw

                if self.down:
                        logger.warn("Entered Maintenance mode. All URLS routed to maintenanceController!")
                        import flagr.controllers.maintenanceController
                else:
                        import flagr.controllers.controllerMap

                fw.serveForever()


if __name__ == "__main__":
        daemon = app(c.pidFolder+c.logName+'.pid')
        daemon.down=False
        if len(sys.argv) >= 2:
                if 'noDaemon' in sys.argv:
                        logger = setupLog()
                        import seshat.framework as fw
                        if 'maintenance' in sys.argv:
                                import flagr.controllers.maintenanceController
                        else:
                                import flagr.controllers.controllerMap
                        fw.serveForever()

                elif 'start' in sys.argv:
                        daemon.start()

                elif 'stop' in sys.argv:
                        daemon.stop()

                elif 'restart' in sys.argv:
                        daemon.restart()

                elif 'maintenance' in sys.argv:
                        daemon.down=True
                        daemon.stop()
                        daemon.start()

                else:
                        print "Unknown command"
                        sys.exit(2)

                sys.exit(0)

        else:
                print "usage: %s start|stop|restart|noDaemon|(noDaemon) maintenance" % sys.argv[0]
                sys.exit(2)
