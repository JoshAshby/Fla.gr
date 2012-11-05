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
import flagr.models.flagModel as fm
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import os

path = os.path.dirname(c.__file__)
import flagr.views.pyStrap.pyStrap as ps
from datetime import datetime as dt

import gevent

import logging
logger = logging.getLogger(c.logName+".flagrConfig")

def _update(message):
    logger.debug("Sending signal: %s" % message)
    zmqc.zmqSock.send(message)
    logger.debug("Signal sent")

def updateSearch(man=False):
    message = "indexUpdate "
    if man:
        message += "now"
    else:
        message += "increase"

    ser = gevent.spawn(_update, message)
    ser.join()

def flagThumbnails(flags, deity=False):
    if flags:
        flagList = ""
        for flag in flags:
            title = ps.baseAnchor("%s %s..." %
                (
                    ps.baseIcon(flag.icon),
                    flag["title"][:10].strip(" ")
                ),
                link=c.baseURL+"/flag/%s"%flag.id)

            if not flag["visibility"]:
                vis = "%s Private" % ps.baseIcon("eye-close")
            else:
                vis = "%s Public" % ps.baseIcon("globe")

            who = ps.baseAnchor(flag["author"],
                link=c.baseURL+"/people/%s"%flag["author"])

            if not deity:
                width = 7
                if c.session.loggedIn and c.session.userID == flag["userID"]:
                    who = ps.baseAnchor("You!",
                        link=c.baseURL+"/you")
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
                else:
                    edit = ""
            else:
                width = 5
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
                width=width)
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

newFlagButton = """
<div class=" pull-right  btn-group ">
    <a class=" btn-info  btn " href="http://localhost/flags/new">
        <i class=" icon-flag "></i> New Flag</a>
    <a class="dropdown-toggle btn-info  btn"
        rel="tooltip"
        href=""
        data-toggle="dropdown"
        data-original-title="Quick select"
        data-placement="bottom">
            <i class="icon-chevron-down"></i>
    </a>
    <ul class=" dropdown-menu ">
        <li>
            <a
                tabindex="-1"
                href="http://localhost/flags/new/note">
                    <i class=" icon-list-alt "></i> Note</a>
        </li>
        <li>
            <a
                tabindex="-1"
                href="http://localhost/flags/new/bookmark">
                    <i class=" icon-bookmark "></i> Bookmark</a>
        </li>
    </ul>
</div>
"""

def tabs(tabs, extra="", classes="tabs"):
    returnHTML = ""
    for tab in tabs:
        html = "<li>"
        if tab.has_key("active"):
            html = "<li class=\"active\">"
        html += """<a href="%(link)s"
    rel="tooltip"
    data-original-tile="%(title)s"
    data-placement="bottom">
        <i class="icon-%(icon)s"></i>
    </a>
</li>
""" % tab
        returnHTML += html

    returnHTML += extra

    return """<ul class="nav nav-%s">
    %s
</ul>""" % (classes, returnHTML)

def listPager(lists, link, members):
    start = int(members["start"]) if members.has_key("start") else 0

    nextClass = ""
    prevClass = ""

    if start == 0:
            prevClass = "disabled"
            prevLink = "#"
    elif start == 10:
            prevLink = c.baseURL+link
    else:
            prevLink = c.baseURL+link + "?start=" + str(start-10)

    if len(lists[start+10:start+20]) <= 0:
            nextClass = "disabled"
            nextLink = "#"
    else:
            nextLink = c.baseURL+link + "?start=" + str(start+10)

    lists = lists[start:start+10]

    pager = """<ul class="pager">
<li class="previous %s">
    <a href="%s">&larr; Previous</a>
</li>
<li class="next %s">
    <a href="%s">Next &rarr;</a>
</li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)

    return lists, pager

def flagSearch(user=None, deity=False, members=[]):
    if members.has_key("search") and members["search"] != "":
        term = members["search"]

        ix = open_dir(path+"/.searchIndex")
        flags = []

        with ix.searcher() as searcher:
            query = MultifieldParser(
                ["title",
                    "description",
                    "labels",
                    "url",
                    "author"],
                ix.schema).parse(unicode(term))
            results = searcher.search(query)

            for result in results:
                flags.append(fm.flag(result["id"]))


        buildMessage = "Uh oh! Looks like I couldn't find any flags at the moment that fit that search criteria."

        if not deity and not user:
            for flag in flags:
                if not flag["visibility"] and flag["userID"] != c.session.userID:
                    flags.pop(flags.index(flag))
        elif user and not deity and user != c.session.userID:
            for flag in flags:
                if not flag["visibility"] and flag["userID"] != c.session.userID and flag["userID"] != user:
                    flags.pop(flags.index(flag))
        elif user and deity:
            for flag in flags:
                if not flag["userID"] == user:
                    flags.pop(flags.index(flag))

        flags, pager = listPager(flags,
            "/search/flags",
            members)

        if flags:
            flagList = flagThumbnails(flags)
        else:
            flagList = buildMessage

        content = ps.baseRow(ps.baseColumn(flagList, id="flags")) + pager

        return content
    return ""
