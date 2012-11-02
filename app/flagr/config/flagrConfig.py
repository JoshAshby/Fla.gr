#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

Flagr related tasks and config options.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import siteConfig.zmqConfig as zmqc

import flagr.views.pyStrap.pyStrap as ps
from datetime import datetime as dt

import gevent

import logging
logger = logging.getLogger(c.logName+".flagrConfig")


def _update():
    logger.debug("Sending signal...")
    zmqc.zmqSock.send("indexUpdate increase")
    logger.debug("Signal sent...")

def _forceUpdate():
    logger.debug("Sending manual update signal...")
    zmqc.zmqSock.send("indexUpdate now")
    logger.debug("Manual update signal sent...")

def updateSearch():
    ser = gevent.spawn(_update)
    ser.join()

def manualUpdateSearch():
    ser = gevent.spawn(_forceUpdate)
    ser.join()

def flagThumbnails(flags):
        if flags:
                flagList = ""
                for flag in flags:
                        title = ps.baseAnchor("%s %s..." %
                                                (ps.baseIcon(flag.icon),
                                                flag["title"][:8].strip(" ")
                                        ),
                                        link=c.baseURL+"/flag/%s"%flag.id)

                        if not flag["visibility"]:
                                vis = "%s Private" % ps.baseIcon("eye-close")
                        else:
                                vis = "%s Public" % ps.baseIcon("globe")

                        who = ps.baseAnchor(flag["author"],
                                link=c.baseURL+"/people/%s"%flag["author"])

                        if c.session.loggedIn and c.session.userID == flag["userID"]:
                                who = ps.baseAnchor("You!",
                                        link=c.baseURL+"/you")
                                who = "You!"
                                edit = ps.baseButtonGroup([
                                        ps.baseAButton("%s" % ps.baseIcon("edit"),
                                                classes="btn-info",
                                                link=c.baseURL+"/flag/%s/edit"%flag.id,
                                                rel="tooltip",
                                                data=[("original-title", "Edit flag"),
                                                ("placement", "bottom")]),
                                        ps.baseAButton("%s" % ps.baseIcon("trash"),
                                                classes="btn-danger",
                                                link=c.baseURL+"/flag/%s/delete"%flag.id,
                                                rel="tooltip",
                                                data=[("original-title", "Delete Flag"),
                                                ("placement", "bottom")])
                                        ])

                        elif c.session.loggedIn:
                                edit = ps.baseButtonGroup([
                                        ])
                        else:
                                edit = ps.baseButtonGroup([
                                        ])

                        caption = ps.baseHeading(title + "   " + ps.baseSmall(
                            ps.baseBold(who, classes="muted")),
                            size=3)
                        time = dt.strptime(flag["time"], "%b-%d-%Y %I:%M %p")
                        time = time.strftime("%b-%d-%y")

                        caption = ps.baseRow([
                            ps.baseColumn(caption, width=3),
                            ps.baseColumn(
                                ps.baseWell(
                                    ps.baseColumn(
                                        ps.baseBold("When:", classes="muted")
                                    ) +
                                    ps.baseColumn(time) +
                                    ps.baseColumn(vis) +
                                    ps.baseColumn(edit, classes="pull-right")
                                ),
                            width=7)
                            ])

                        caption += "%s" % flag["description"][:250]

                        labelLinks = ""

                        if flag["labels"]:
                                for label in flag["labels"]:
                                        labelLinks += ps.baseAnchor(
                                            ps.baseLabel(label,
                                                classes="label-info"),
                                            link=c.baseURL+"/label/"+label) + " "

                        for field in flag.fields:
                                name = field[0] if type(field) != str else field
                                if name not in ["title",
                                    "description",
                                    "labels",
                                    "time",
                                    "visibility",
                                    "author",
                                    "userID",
                                    "flagType"]:
                                        if name in ["url"]:
                                                d = flag[name]
                                                value = ps.baseAnchor(d, link=d)
                                        else:
                                                value = flag[name]
                                        caption += "%s: %s" %(
                                            ps.baseBold(name.lower().title(),
                                                classes="muted"),
                                            value)

                        caption += ps.baseRow([
                                ps.baseColumn(
                                    ps.baseBold("Labels: ", classes="muted")
                                ),
                                ps.baseColumn(labelLinks)
                        ])

                        typeOfFlag = flag["flagType"]

                        flagList += """<div class="%s">"""%typeOfFlag + caption + "<hr>" + """</div>"""

                return flagList
        else:
                return ""

def deityFlagThumbnails(flags):
        if flags:
                flagList = ""
                for flag in flags:
                        title = ps.baseAnchor("%s %s..." % (
                            ps.baseIcon(flag.icon),
                            flag["title"][:8].strip(" ")
                        ), link=c.baseURL+"/flag/%s"%flag.id)

                        if not flag["visibility"]:
                                vis = "%s Private" % ps.baseIcon("eye-close")
                        else:
                                vis = "%s Public" % ps.baseIcon("globe")

                        who = ps.baseAnchor(flag["author"],
                                link=c.baseURL+"/people/%s"%flag["author"])
                        edit = ps.baseButtonGroup([
                                ps.baseAButton("%s" % ps.baseIcon("edit"),
                                        classes="btn-info btn-small",
                                        link=c.baseURL+"/flag/%s/edit"%flag.id,
                                        rel="tooltip",
                                        data=[("original-title", "Edit flag"),
                                        ("placement", "bottom")]),
                                ps.baseAButton("%s" % ps.baseIcon("trash"),
                                        classes="btn-danger btn-small",
                                        link=c.baseURL+"/flag/%s/delete"%flag.id,
                                        rel="tooltip",
                                        data=[("original-title", "Delete Flag"),
                                        ("placement", "bottom")])
                                ])

                        caption = ps.baseHeading(title + "   " + ps.baseSmall(
                                ps.baseBold(who, classes="muted")
                            ), size=3)

                        time = dt.strptime(flag["time"], "%b-%d-%Y %I:%M %p")
                        time = time.strftime("%b-%d-%y")

                        caption = ps.baseRow([
                            ps.baseColumn(caption, width=3),
                            ps.baseColumn(
                                ps.baseWell(
                                    ps.baseColumn(
                                        ps.baseBold("When:", classes="muted")
                                    ) +
                                    ps.baseColumn(time) +
                                    ps.baseColumn(vis) +
                                    ps.baseColumn(edit, classes="pull-right")
                                ),
                            width=5)
                            ])

                        caption += "%s<br />" % flag["description"][:250]

                        labelLinks = ""

                        if flag["labels"]:
                                for label in flag["labels"]:
                                        labelLinks += ps.baseAnchor(
                                            ps.baseLabel(label,
                                                classes="label-info"),
                                            link=c.baseURL+"/label/"+label) + " "

                        for field in flag.fields:
                                name = field[0] if type(field) != str else field
                                if name not in ["title",
                                    "description",
                                    "labels",
                                    "time",
                                    "visibility",
                                    "author",
                                    "userID",
                                    "flagType"]:
                                        if name in ["url"]:
                                                d = flag[name]
                                                value = ps.baseAnchor(d,
                                                    link=d)
                                        else:
                                                value = flag[name]
                                        caption += "%s: %s" %(
                                            ps.baseBold(name.lower().title(),
                                                classes="muted"),
                                            value)

                        caption += ps.baseRow([
                                ps.baseColumn(
                                    ps.baseBold("Labels: ", classes="muted")
                                ),
                                ps.baseColumn(labelLinks)
                        ])

                        flagList += caption + "<hr>"

                return flagList
        else:
                return ""
