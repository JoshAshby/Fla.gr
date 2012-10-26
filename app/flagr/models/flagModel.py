#!/usr/bin/env python2
"""
Fla.gr - Personal Memory
Interface model for working with flag models.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import flagr.config.dbConfig as fdbc
import flagr.models.flags.flags as bf
import models.blocks.helpers as helpers
import markdown


def flag(id=None, flagType=None, md=False):
        if id:
                id = id.strip("flag:")

        if id and not flagType:
                key = "flag:"+id.strip("flag:")
                flagType = fdbc.redisFlagServer.get(key+":flagType")
                returnFlag = getattr(bf, flagType.lower()+"Flag")(id)
                if md:
                        returnFlag["description"] = markdown.markdown(returnFlag["description"])
                return returnFlag

        if id and flagType:
                raise Exception("Can't mutate a flag! To mutate, supply id and mutate in code, but not here!")

        if not id and flagType:
                return pushFlag(flagType)

        if not id and not flagType:
                raise Exception("No id or flagType supplied. Nothing to do...")

def pushFlag(flagType=None):
        if flagType:
                flag = getattr(bf, flagType.lower()+"Flag")()
                return flag
        else:
                raise Exception("No flagType supplied, aborting!")

def flagList(userID=None, md=False, flags=[]):
        keys = fdbc.redisFlagServer.keys("flag:*:id")
        flagList = []
        def addFlag(key):
                returnFlag = flag(key)
                if md:
                        returnFlag["description"] = markdown.markdown(returnFlag["description"])

                flagList.append(returnFlag)

        if not flags:
                """
                #global flag search - everyone but yours
                if visible and not yours:
                        throw it into the list
                """
                if not userID:
                        for key in keys:
                                key = key.strip(":id")
                                if helpers.boolean(fdbc.redisFlagServer.get(key+":visibility")):
                                        addFlag(key)

                """
                #global flag search for one users flag
                if visible and the userID matches the userID we're looking for:
                        throw it into the list
                """
                if userID and userID != c.session.userID:
                        for key in keys:
                                key = key.strip(":id")
                                if helpers.boolean(fdbc.redisFlagServer.get(key+":visibility")) and c.redisFlagServer.get(key+":userID") == userID:
                                        addFlag(key)

                """
                #looking for just your flags
                if it's yours:
                        throw it into the list
                """
                if userID and userID == c.session.userID:
                        for key in keys:
                                key = key.strip(":id")
                                if fdbc.redisFlagServer.get(key+":userID") == c.session.userID:
                                        addFlag(key)
        else:
                """
                Someone wants specific flags so it's assumed they
                are only going to show proper flags
                """
                for key in flags:
                        key = key.strip("flag::id")
                        addFlag(key)

        return flagList
