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
zmqSock.bind("tcp://127.0.0.1:5000")
