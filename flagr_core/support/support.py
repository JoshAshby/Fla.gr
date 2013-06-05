#!/usr/bin/env python
"""
fla.gr service daemon controllers.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import sys
import os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import config.config as c

from utils.simpleDaemon import Daemon


def setupLog(daemon):
    """
    Sets up the main logger for the daemon
    """
    import logging
    level = logging.WARNING
    if c.general.debug:
        level = logging.DEBUG

    formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
    %(message)s""")

    logger = logging.getLogger(c.general.logName+daemon)
    logger.setLevel(level)

    fh = logging.FileHandler(c.general.dirs["logDir"]+c.general.logName+daemon+".log")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if c.general.debug and "noDaemon" in sys.argv:
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


class searchIndex(Daemon):
    def run(self):
        logger = setupLog("search")
        __import__("utils.search.searchIndexer", siu, locals())
        siu.start()

class emailSender(Daemon):
    def run(self):
        logger = setupLog("email")
        __import__("utils.email.emailSender", ems, locals())
        ems.start()


if __name__ == "__main__":
    if sys.argv:
        noDaemon = False
        if 'noDaemon' in sys.argv:
            noDaemon = True

        if 'search' == sys.argv[1]:
            if 'build' in sys.argv:
                logger = setupLog("search")
                import utils.search.searchIndexer as siu
                siu.buildIndexes()
                sys.exit(0)

        if not noDaemon:
            if 'search' == sys.argv[1]:
                daemon = searchIndex(c.general.dirs["pidDir"]+c.general.logName+'SearchDaemon.pid', stderr=c.general.files["stderr"])
            elif 'email' == sys.argv[1]:
                daemon = emailSender(c.general.dirs["pidDir"]+c.general.logName+'emailDaemon.pid', stderr=c.general.files["stderr"])

            if 'start' in sys.argv:
                daemon.start()

            elif 'stop' in sys.argv:
                daemon.stop()

            elif 'restart' in sys.argv:
                daemon.restart()

            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)

        else:
            if 'search' == sys.argv[1]:
                logger = setupLog("search")
                import utils.search.searchIndexer as siu
                siu.start()
            elif 'email' == sys.argv[1]:
                logger = setupLog("email")
                import utils.email.emailSender as ems
                ems.start()
            sys.exit(0)

    else:
        print "usage: %s start|stop|restart|noDaemon" % sys.argv[0]
        sys.exit(2)
