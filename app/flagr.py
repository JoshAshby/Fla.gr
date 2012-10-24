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
import sys
import signal
import daemon
import lockfile
import sys
import os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

debug = True
logFolder = "/var/log/python/"
pidFolder = "/tmp/"

def setupLog():
        import logging
        level = logging.WARNING
        if debug:
                level = logging.DEBUG

        formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
                %(message)s""")

        logger = logging.getLogger("flagr")
        logger.setLevel(level)

        fh = logging.FileHandler(logFolder+"flagr.log")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        if debug and "noDaemon" in sys.argv:
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

from simpleDaemon import Daemon
class app(Daemon):
        down = False
        def run(self):
                setupLog()
                import seshat.framework as fw

                if self.down:
                        import controllers.maintenanceController
                else:
                        import controllers.controllerMap

                fw.forever()


if __name__ == "__main__":
        daemon = app(pidFolder+'flagr.pid')
        daemon.down=False
        if len(sys.argv) >= 2:
                if 'noDaemon' in sys.argv:
                        setupLog()
                        import seshat.framework as fw
                        if 'maintenance' in sys.argv:
                                import controllers.maintenanceController
                        else:
                                import controllers.controllerMap
                        fw.forever()

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
