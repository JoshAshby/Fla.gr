#!/usr/bin/env python
"""
Aid to get flagr setup and running

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.couch.user.userModel as um
import gators.firstTimeGator.config as config

def setup():
    print "Setting up fla.gr from config/initial.json..."
    initialSetup()
    bucketSetup()
    print "Done"

def initialSetup():
    print "Setting up inital users, flags and templates..."
    if config.initial.has_key("users"):
        for user in config.initial["users"]:
            newUser = um.userORM(user["username"], user["password"])
            print "\tAdding new user `%s`"%user["username"]
            print "\t\tpassword `%s`"%user["password"]
            if user.has_key("level"):
                print "\t\tlevel `%d`"%user["level"]
                newUser.level = user["level"]
            else:
                print "\t\tlevel `100` - god"
                newUser.level = 100
            newUser.save()

    if config.initial.has_key("flags"):
        pass

    if config.initial.has_ley("templates"):
        pass

def bucketSetup():
    print "Now setting up buckets..."


if __name__ == "__main__":
    setup()
