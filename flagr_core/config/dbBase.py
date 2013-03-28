#!/usr/bin/env python
"""
fla.gr database setup
Handles getting all the database pools going so it's easy to use
throughout the rest of fla.gr
"""
import redis
from couchdb import Server

server = Server('http://localhost:5984/')
"""
Where is our CouchDB located at?
"""
couchServer = server['flagr']
"""
Which database on CouchDB do we want to use?
"""

redisSessionServer = redis.Redis("localhost", db=3)
"""
Where in redis is the database for sessions to be stored in?
"""
redisBucketServer = redis.Redis("localhost", db=4)
"""
Where in redis is the database for Buckets and Settings to be stored in?
"""
