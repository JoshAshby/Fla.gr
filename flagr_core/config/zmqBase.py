#!/usr/bin/env python
"""
Settings and initalization of the zmq socket for fla.gr
This is used by the main app.py process.
"""
from gevent_zeromq import zmq

context = zmq.Context()
zmqSock = context.socket(zmq.PUB)

zmqSock.bind("tcp://127.0.0.1:5000")
"""
Where are we binding our ZeroMQ socket?
"""
