#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Config settings

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
from gevent_zeromq import zmq

context = zmq.Context()
zmqSock = context.socket(zmq.PUB)
zmqSock.bind("tcp://127.0.0.1:5000")
