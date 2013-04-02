#!/usr/bin/env python
"""
Test case for making sure that the various models are
working correctly.
"""
import nose.tools as nst

import models.user.userModel as um
import bcrypt
import models.modelExceptions.userModelExceptions as umExceptions

import config.dbBase as db

import models.template.templateModel as tm
import models.setting.settingModel as sm
import models.request.requestModel as rm
import models.flag.flagModel as fm
import models.bucket.bucketModel as bm
import models.basic.sessionModel as session


class dummyRedisServer(object):
    """
    Dummy redis server object which tries to emulate the redis wrapper
    as best as possible, allowing for the seperation of tests, for both couch
    and redis.
    """
    def __init__(self, *args, **kwargs):
        self._items = []
        pass

    def hset(self, key, value):
        self._items[key] = value

    def hget(self, key):
        return self._items[key]


def setUp_redisDummy():
    """
    Sets up the models to use a dummy redis server
    """
    db.redisSessionServer = dummyRedisServer()
    db.redisBucketServer = dummyRedisServer()

def test_userModel(self):
    """
    Unittest for userModels. Creates a new user then saves and makes sure user
    data matches initial data. Then uses various methods to find and edit the user
    then finally cleans up and deletes the created user.
    """
    password = "test"
    username = "Test"
    about = """#This is a test  
  
User profile about.
    """

    newUser = um.userORM.new(username, password)

    assert newUser.username == username
    assert newUser.password == bcrypt.hashpw(password, newUser.password)

    newUser.save()

    newUser_find = um.userORM.find(username)
    assert newUser_find == newUser

    newUser_find.about = about
    assert newUser_find.about == about

    newUser_find.save()

    newUser = um.userORM.getByID(newUser_find.id)

    assert newUser == newUser_find

    newUser.setPassword("test")
    assert newUser.password == bcrypt.hashpw("test", newUser.password)

    newUser.delete()
