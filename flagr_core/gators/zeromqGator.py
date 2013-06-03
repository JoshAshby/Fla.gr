#!/usr/bin/env python
"""
Settings and initalization of zmq socket for fla.gr

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from gevent_zeromq import zmq

context = zmq.Context()
zmqSock = context.socket(zmq.PUB)

from gators.baseGator import baseGator


class config(baseGator):
    baseFile = 'zeromq.json'
    _temp = {}
    def postInit(self):
        self._temp["sock"] = zmqSock.bind(self._data["URL"]+":"+str(self._data["port"]))
        self._data = self._temp
