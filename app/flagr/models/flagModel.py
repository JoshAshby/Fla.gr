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
import siteConfig.dbConfig as dbc
import flagr.models.flags.flags as bf
import models.blocks.helpers as helpers
import markdown


def flag(id=None, flagType=None, md=False):
        if id:
                id = id.strip("flag:")

        if id and not flagType:
                key = "flag:"+id.strip("flag:")
                flagType = dbc.redisFlagServer.get(key+":flagType")
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

def flagList(userID=None, md=False, flags=[], private=False, public=False, deity=False):
        keys = dbc.redisFlagServer.keys("flag:*:id")
        flagList = []
        def addFlag(key):
                returnFlag = flag(key)
                if md:
                        returnFlag["description"] = markdown.markdown(returnFlag["description"])

                flagList.append(returnFlag)

        if not flags:
            if not deity:
                """
                #global flag search - everyone but yours
                if visible and not yours:
                        throw it into the list
                """
                if not userID:
                        for key in keys:
                                key = key.strip(":id")
                                if helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                        addFlag(key)

                """
                #global flag search for one users flag
                if visible and the userID matches the userID we're looking for:
                        throw it into the list
                """
                if userID and userID != c.session.userID:
                        for key in keys:
                                key = key.strip(":id")
                                if helpers.boolean(dbc.redisFlagServer.get(key+":visibility")) and dbc.redisFlagServer.get(key+":userID") == userID:
                                        addFlag(key)

                """
                #looking for just your flags
                if it's yours:
                        throw it into the list
                """
                if userID and userID == c.session.userID:
                        for key in keys:
                                key = key.strip(":id")
                                if dbc.redisFlagServer.get(key+":userID") == c.session.userID:
                                        if public:
                                                if helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                                        addFlag(key)
                                        elif private:
                                                if not helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                                        addFlag(key)
                                        else:
                                                addFlag(key)
            else:
                if not userID:
                        for key in keys:
                                key = key.strip(":id")
                                if public:
                                        if helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                                addFlag(key)
                                elif private:
                                        if not helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                                addFlag(key)
                                else:
                                        addFlag(key)

                else:
                        for key in keys:
                                key = key.strip(":id")
                                if dbc.redisFlagServer.get(key+":userID") == userID:
                                        if public:
                                                if helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                                        addFlag(key)
                                        elif private:
                                                if not helpers.boolean(dbc.redisFlagServer.get(key+":visibility")):
                                                        addFlag(key)
                                        else:
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
