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
import siteConfig as sc
import views.pyStrap.pyStrap as ps
from whoosh.index import create_in
from whoosh.fields import *
import flagr.models.flagModel as fm
from whoosh.index import open_dir
import gevent

import logging
logger = logging.getLogger("flagr.flagrConfig")


def _update():
        logger.debug("Sending signal...")
        sc.zmqSock.send("indexUpdate increase")
        logger.debug("Signal sent...")

def updateSearch():
        ser = gevent.spawn(_update)
        ser.join()

def flagThumbnails(flags, width=10):
        if flags:
                flagList = ""
                for flag in flags:
                        title = ps.baseAnchor("%s %s" % (ps.baseIcon(flag.icon), flag.title), link=c.baseURL+"/flag/%s"%flag.id)

                        if not flag["visibility"]:
                                vis = "%s Private" % ps.baseIcon("eye-close")
                        else:
                                vis = "%s Public" % ps.baseIcon("globe")

                        who = ps.baseAnchor(flag["author"], link=c.baseURL+"/people/%s"%flag["author"])

                        if c.session.loggedIn and c.session.userID == flag["userID"]:
                                who = ps.baseAnchor("You!", link=c.baseURL+"/you")
                                edit = ps.baseSplitDropdown(btn=
                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                link=c.baseURL+"/flag/%s"%flag.id,
                                                classes="",
                                                rel="tooltip",
                                                data=[("original-title", "View this flag")])+
                                        ps.baseAButton("%s" % ps.baseIcon("edit"),
                                                classes="btn-info",
                                                link=c.baseURL+"/flag/%s/edit"%flag.id,
                                                rel="tooltip",
                                                data=[("original-title", "Edit this flag")])
                                        ,
                                        dropdown=ps.baseMenu(name="flagDropdown",
                                                items=[{"name": "%s Copy flag" % ps.baseIcon("copy"),
                                                        "link": c.baseURL+"/flag/%s/copy"%flag.id},
                                                {"name": ps.baseBold("%s Delete flag" % ps.baseIcon("trash"),
                                                        classes="text-error"),
                                                        "link": c.baseURL+"/flag/%s/delete"%flag.id}]
                                                ),
                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                classes="dropdown-toggle btn-danger",
                                                data=[("toggle", "dropdown"),
                                                        ("original-title", "More actions")],
                                                rel="tooltip"), classes="pull-right")

                        elif c.session.loggedIn:
                                edit = ps.baseButtonGroup([
                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                        link=c.baseURL+"/flag/%s"%flag.id,
                                                        classes="", rel="tooltip", data=[("original-title", "View this flag")]),
                                        ps.baseAButton(ps.baseIcon("copy"),
                                                link=c.baseURL+"/flag/%s/copy"%flag.id,
                                                classes="",
                                                rel="tooltip",
                                                data=[("original-title", "Copy this flag")])
                                        ])
                        else:
                                edit = ps.baseButtonGroup([
                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                        link=c.baseURL+"/flag/%s"%flag.id,
                                                        classes="", rel="tooltip", data=[("original-title", "View this flag")])
                                        ], classes="pull-right")

                        caption = ps.baseHeading(title, size=3)

                        caption += ps.baseRow(ps.baseColumn(ps.baseWell(
                                ps.baseColumn(ps.baseBold("Author:", classes="muted")) +
                                ps.baseColumn(who) +
                                ps.baseColumn(ps.baseBold("When:", classes="muted")) +
                                ps.baseColumn(flag["time"]) +
                                ps.baseColumn(vis) +
                                ps.baseColumn(edit, classes="pull-right")
                        ), width=width))

                        caption += "%s%s<br />" % (flag["description"][:250], ps.baseAnchor("...", link=c.baseURL+"/flag/%s"%flag.id))

                        labelLinks = ""

                        if flag["labels"]:
                                for label in flag["labels"]:
                                        labelLinks += ps.baseAnchor(ps.baseLabel(label, classes="label-info"), link=c.baseURL+"/label/"+label) + " "

                        for field in flag.fields:
                                name = field[0] if type(field) != str else field
                                if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                        if name in ["url"]:
                                                d = flag[name]
                                                value = ps.baseAnchor(d, link=d)
                                        else:
                                                value = flag[name]
                                        caption += "%s: %s" %(ps.baseBold(name.lower().title(), classes="muted"), value)

                        caption += ps.baseRow([
                                ps.baseColumn(ps.baseBold("Labels: ", classes="muted")),
                                ps.baseColumn(labelLinks)
                        ])

                        flagList += caption + "<hr>"

        return flagList


def flagIndex():
        ix = open_dir("index")
        writer = ix.writer()

        for key in r.keys("flag:*:id"):
                flag = fm.flag(key.strip(":id"))
                labels = ""
                for label in flag["labels"]:
                        labels += "%s ,"%label

                labels = labels.strip(", ")

                url = u""

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                if name in ["url"]:
                                        url = flag["url"]

                writer.add_document(title=flag["title"],
                                id=unicode(flag.id),
                                description=flag["description"],
                                labels=labels,
                                url=url,
                                author=flag["author"],
                                userID=unicode(flag["userID"]),
                                time=flag["time"])

        writer.commit()

def flagIndexSetup():
        schema = Schema(title=TEXT(stored=True),
                        id=ID(stored=True, unique=True),
                        description=TEXT,
                        labels=KEYWORD(stored=True),
                        url=TEXT(stored=True),
                        author=TEXT(stored=True),
                        time=TEXT,
                        userID=TEXT)

        if not os.path.exists("index"):
                os.mkdir("index")

        ix = create_in("index", schema)
        writer = ix.writer()
        writer.commit()
