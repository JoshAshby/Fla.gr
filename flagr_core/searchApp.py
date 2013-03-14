#!/usr/bin/env python
"""
fla.gr search index daemon controller.

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


def setupLog():
        """
        Sets up the main logger for the daemon
        """
        import logging
        level = logging.WARNING
        if c.debug:
                level = logging.DEBUG

        formatter = logging.Formatter("""%(asctime)s - %(name)s - %(levelname)s
        %(message)s""")

        logger = logging.getLogger(c.logName+".search")
        logger.setLevel(level)

        fh = logging.FileHandler(c.logFolder+c.logName+"Search.log")
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


class searchIndex(Daemon):
    def run(self):
        setupLog()
        import search.searchController as siu
        siu.start()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        noDaemon = False
        if 'noDaemon' in sys.argv:
            noDaemon = True

        if 'search' == sys.argv[1]:
            if 'build' in sys.argv:
                setupLog()
                import search.searchController as siu
                siu.buildIndexes()
                sys.exit(0)

            if noDaemon:
                daemon = searchIndex(c.pidFolder+c.logName+'SearchDaemon.pid')

                if 'start' in sys.argv:
                    daemon.start()

                elif 'stop' in sys.argv:
                    daemon.stop()

                elif 'restart' in sys.argv:
                    daemon.restart()

                else:
                    print "Unknown command"
                    sys.exit(2)

            else:
                setupLog()
                import search.searchController as siu
                siu.start()

        sys.exit(0)

    else:
        print "usage: %s start|stop|restart|noDaemon" % sys.argv[0]
        sys.exit(2)
