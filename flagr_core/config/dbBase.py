#!/usr/bin/env python
"""
fla.gr database setup

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import redis
from couchdb import Server

server = Server('http://localhost:5984/')
couchServer = server['flagr']

redisSessionServer = redis.Redis("localhost", db=3)
redisBucketServer = redis.Redis("localhost", db=4)
