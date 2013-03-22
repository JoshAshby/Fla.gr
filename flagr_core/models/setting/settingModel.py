#!/usr/bin/env python
"""
fla.gr request model for managing site wide settings
    This is more just so each module in the admin panel
    can have a standard way of setting and retrieving settings

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.dbBase as db


def setSetting(featureName, settingName, value):
    """
    This may or may not work the way I'm hoping for it to...
    Should update the given buckets settings to value

    :param bucketName: The bucket name to update the settings for
    :param settingName: The name of the settings, if this key exists then a type check will happen against `value`
    :param value: The value of the setting, should match type of setting if settingName exists in the db already
    """
    settingKey = "setting:%s:%s"%(featureName, settingName)
    if db.redisBucketServer.exists(settingKey):
        settingType = db.redisBucketServer.type(settingKey)

        if type(value) == str:
            if settingType and settingType == "str":
                db.redisBucketServer.set(settingKey, value)
            elif not settingType:
                db.redisBucketServer.set(settingKey, value)
            else:
                raise Exception("Value and key are of different types")
        elif type(value) == set:
            if settingType and settingType == "set":
                currentMembers = db.redisBucketServer.smembers(settingKey)
                for member in currentMembers.difference(value):
                    db.redisBucketServer.srem(settingKey, member)
                    currentMembers.remove(member)
                for member in value.difference(currentMembers):
                    db.redisBucketServer.sadd(settingKey, member)
            elif not settingType:
                for member in value:
                    db.redisBucketServer.sadd(settingKey, member)
            else:
                raise Exception("Value and key are of different types")
    else:
        if type(value) == set:
            for item in value:
                db.redisBucketServer.sadd(settingKey, item)
        elif type(value) == str:
            db.redisBucketServer.set(settingKey, value)
        else:
            raise Exception("Unknown setting data type")


def getSetting(featureName, settingName):
    """

    """
    settingKey = "setting:%s:%s"%(featureName, settingName)
    if db.redisBucketServer.exists(settingKey):
        keyType = db.redisBucketServer.type(settingKey)

        if keyType == "string":
            return db.redisBucketServer.get(settingKey)
        elif keyType == "set":
            return db.redisBucketServer.smembers(settingKey)
    else:
        raise Exception("Setting doesn't exist!")

