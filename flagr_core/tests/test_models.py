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
    testCookieID = "0000"

    newUser = um.userORM(username, password)
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

    newUser.loginThis(testCookieID)
    assert newUser.loggedIn
    assert newUser.sessionID == testCookieID

    newUser.logout()
    assert newUser.loggedIn == False

    assert newUser.getAlerts() == ""
    newUser.pushAlert("test", "test", "error", "next")

    assert newUser.getAlerts()

    newUser.clearAlerts()
    assert newUser.getAlerts() == ""

    newUser.pushAlert("test", "test", "error", "later")
    assert newUser.getAlerts()

    newUser.clearAlerts()
    assert newUser.getAlerts()

    newUser.alerts = []
    newUser.saveAlerts()

    newUser.delete()
