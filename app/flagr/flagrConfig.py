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
import views.pyStrap.pyStrap as ps

def flagThumbnails(flags, width=10):
        if flags:
                flagList = ""
                for flag in flags:
                        title = ps.baseAnchor("%s %s" % (ps.baseIcon(flag.icon), flag.title), link=c.baseURL+"/flags/view/"+flag.id)

                        if not flag["visibility"]:
                                other = ps.baseLabel("%s Private" % ps.baseIcon("eye-close"))
                        else:
                                other = ps.baseAnchor(ps.baseLabel("%s Public" % ps.baseIcon("globe")), link=c.baseURL+"/labels/view/public")

                        caption = "%s%s<br />" % (flag["description"][:250], ps.baseAnchor("...", link=c.baseURL+"/flags/view/"+flag.id))

                        for field in flag.fields:
                                name = field[0] if type(field) != str else field
                                if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                        if name in ["url"]:
                                                d = flag[name]
                                                value = ps.baseAnchor(d, link=d)
                                        else:
                                                value = flag[name]
                                        caption += "%s: %s" %(ps.baseBold(name.lower().title(), classes="muted"), value)

                        who = flag["author"]

                        if c.session.loggedIn and c.session.userID == flag["userID"]:
                                who = "You!"
                                edit = ps.baseSplitDropdown(btn=(
                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                link=c.baseURL+"/flags/view/"+flag.id,
                                                classes="",
                                                rel="tooltip",
                                                data=[("original-title", "View this flag")])+
                                        ps.baseAButton("%s" % ps.baseIcon("edit"),
                                                classes="btn-info",
                                                link=c.baseURL+"/flags/edit/"+flag.id,
                                                rel="tooltip",
                                                data=[("original-title", "Edit this flag")])
                                        ),
                                        dropdown=ps.baseMenu(name="flagDropdown",
                                                items=[{"name": "%s Copy flag" % ps.baseIcon("copy"),
                                                        "link": c.baseURL+"/flags/copy/"+flag.id},
                                                {"name": ps.baseBold("%s Delete flag" % ps.baseIcon("trash"),
                                                        classes="text-error"),
                                                        "link": c.baseURL+"/flags/delete/"+flag.id}]
                                                ),
                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                classes="dropdown-toggle btn-danger",
                                                data=[("toggle", "dropdown"),
                                                        ("original-title", "More actions")],
                                                rel="tooltip"), classes="pull-right")

                        elif c.session.loggedIn:
                                edit = ps.baseButtonGroup([
                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                        link=c.baseURL+"/flags/view/"+flag.id,
                                                        classes="", rel="tooltip", data=[("original-title", "View this flag")]),
                                        ps.baseAButton(ps.baseIcon("copy"),
                                                link=c.baseURL+"/flags/copy/"+flag.id,
                                                classes="",
                                                rel="tooltip",
                                                data=[("original-title", "Copy this flag")])
                                        ])
                        else:
                                edit = ps.baseButtonGroup([
                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                        link=c.baseURL+"/flags/view/"+flag.id,
                                                        classes="", rel="tooltip", data=[("original-title", "View this flag")])
                                        ], classes="pull-right")

                        caption += ps.baseRow([
                                ps.baseColumn(ps.baseBold("Author: ", classes="muted")),
                                ps.baseColumn(who)
                                ])

                        labelLinks = "%s " % other
                        for label in flag["labels"]:
                                labelLinks += ps.baseAnchor(ps.baseLabel(label, classes="label-info"), link=c.baseURL+"/labels/view/"+label) + " "

                        caption += ps.baseRow([
                                ps.baseColumn(ps.baseBold("Labels: ", classes="muted"), width=1),
                                ps.baseColumn(labelLinks)
                        ])

                        title = ps.baseRow([ps.baseColumn(title), ps.baseColumn(edit, classes="pull-right")])
                        if who != "you":
                                who = ""

                        flagList += ps.baseTextThumbnail(label=title, caption=caption, classes="span%s %s"%(width, who))
        return flagList
