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
import redis

redisSessionServer = redis.Redis("localhost", db=1)
redisUserServer = redis.Redis("localhost", db=0)
