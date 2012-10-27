#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

Label data model

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import siteConfig.dbConfig as dbc
import flagr.models.flagModel as fm
import models.blocks.helpers as helpers
import flagr.views.pyStrap.pyStrap as ps
import re

def label(name, count=None):
        returnLabel = " "
        returnLabel += ps.baseAnchor(ps.baseLabel(name, classes="label-info"), link=c.baseURL+"/label/"+name)
        returnLabel += " "
        return returnLabel

def labelList(user=None):
        labelList = set()
        returnLabels = ""

        keys = dbc.redisFlagServer.keys("flag:*:labels")

        if not user:
                for key in keys:
                        if helpers.boolean(dbc.redisFlagServer.get(key.strip(":labels")+":visibility")):
                                labels = dbc.redisFlagServer.smembers(key)
                                labelList = labelList.union(labels)
        else:
                if user == c.session.userID:
                        for key in keys:
                                if dbc.redisFlagServer.get(key.strip(":labels")+":userID") == user:
                                        labels = dbc.redisFlagServer.smembers(key)
                                        labelList = labelList.union(labels)
                else:
                        for key in keys:
                                if helpers.boolean(dbc.redisFlagServer.get(key.strip(":labels")+":visibility")) and dbc.redisFlagServer.get(key.strip(":labels")+":userID") == user:
                                        labels = dbc.redisFlagServer.smembers(key)
                                        labelList = labelList.union(labels)

        for lab in labelList:
                returnLabels += label(lab)

        return returnLabels

def labelsUnderList(labs):
        labelList = set()
        returnLabels = ""

        keys = dbc.redisFlagServer.keys("flag:*:labels")

        reg = re.compile("(^%s/*)"%labs)

        for key in keys:
                if dbc.redisFlagServer.get(key.strip(":labels")+":userID") == c.session.userID:
                        labels = dbc.redisFlagServer.smembers(key)
                        labelList = labelList.union(labels)

                else:
                        if helpers.boolean(dbc.redisFlagServer.get(key.strip(":labels")+":visibility")):
                                labels = dbc.redisFlagServer.smembers(key)
                                labelList = labelList.union(labels)

        for lab in labelList:
                if lab != labs and reg.match(lab):
                        returnLabels += label(lab)

        return returnLabels

def labeledFlagList(label, md=True):
        flagList = []

        keys = dbc.redisFlagServer.keys("flag:*:labels")

        reg = re.compile("(^%s$)" % label)

        for key in keys:
                if dbc.redisFlagServer.get(key.strip(":labels")+":userID") == c.session.userID:
                        labels = dbc.redisFlagServer.smembers(key)
                        for label in labels:
                                if reg.match(label):
                                        flagList.append(key.strip(":labels").strip("flag:"))

                else:
                        if helpers.boolean(dbc.redisFlagServer.get(key.strip(":labels")+":visibility")):
                                labels = dbc.redisFlagServer.smembers(key)
                                for label in labels:
                                        if reg.match(label):
                                                flagList.append(key.strip(":labels").strip("flag:"))
        if flagList:
                flags = fm.flagList(flags=flagList, md=md)
        else:
                flags = ""

        return flags

