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
import config.config as c


def setSetting(featureName, settingName, value):
    """
    This may or may not work the way I'm hoping for it to...
    Should update the given buckets settings to value

    :param bucketName: The bucket name to update the settings for
    :param settingName: The name of the settings, if this key exists then a type check will happen against `value`
    :param value: The value of the setting, should match type of setting if settingName exists in the c.database already
    """
    settingKey = "setting:%s:%s"%(featureName, settingName)
    if c.database.redisBucketServer.exists(settingKey):
        settingType = c.database.redisBucketServer.type(settingKey)

        if type(value) == set:
            if settingType and settingType == "set":
                currentMembers = c.database.redisBucketServer.smembers(settingKey)
                for member in currentMembers.difference(value):
                    c.database.redisBucketServer.srem(settingKey, member)
                    currentMembers.remove(member)
                for member in value.difference(currentMembers):
                    c.database.redisBucketServer.sadd(settingKey, member)
            elif not settingType:
                for member in value:
                    c.database.redisBucketServer.sadd(settingKey, member)
            else:
                raise Exception("Value and key are of different types: %s %s"%(type(value), settingType))
        else:
            c.database.redisBucketServer.set(settingKey, value)

    else:
        if type(value) == set:
            for item in value:
                c.database.redisBucketServer.sadd(settingKey, item)
        else:
            c.database.redisBucketServer.set(settingKey, value)


def getSetting(featureName, settingName):
    """

    """
    settingKey = "setting:%s:%s"%(featureName, settingName)
    if c.database.redisBucketServer.exists(settingKey):
        keyType = c.database.redisBucketServer.type(settingKey)

        if keyType == "string":
            return c.database.redisBucketServer.get(settingKey)
        elif keyType == "set":
            return c.database.redisBucketServer.smembers(settingKey)
    else:
        raise Exception("Setting doesn't exist!")

