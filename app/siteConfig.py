from gevent_zeromq import zmq
context = zmq.Context()
zmqSock = context.socket(zmq.PUB)
zmqSock.bind("tcp://127.0.0.1:5000")
