#!/usr/bin/env python
"""
Test case for making sure that the various models are
working correctly.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import nose.tools as nst

import models.user.userModel as um
import bcrypt
import models.modelExceptions.userModelExceptions as umExceptions

import models.template.templateModel as tm
import models.setting.settingModel as sm
import models.request.requestModel as rm
import models.flag.flagModel as fm
import models.bucket.bucketModel as bm
import models.basic.sessionModel as session


def test_userModel(self):
    password = "test"
    username = "Test"
    about = """#This is a test  
  
User profile about.
    """

    newUser = um.userORM.new(username, password)

    assert newUser.username == username
    assert newUser.password == bcrypt.hashpw(password, newUser.password)

    newUser.save()

    secondUser = um.userORM.find(username)
    assert secondUser == newUser

    secondUser.about = about
    assert secondUser.about == about

    secondUser.save()

    thirdUser = um.userORM.find(username)
    assert thirdUser.about == about

    assert thirdUser == secondUser
