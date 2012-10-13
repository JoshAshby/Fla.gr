#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

Flag controller. Everything under the /flags
        URL is handled and fleshed out, or linked to
        from here.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

import flagr.models.flagModel as fm

from flagr.objects.flagrObject import flagrObject as flagrPage
from seshat.route import route

import views.pyStrap.pyStrap as ps
import flagr.flagrConfig as fc


@route("/you/flags")
@route("/your/flags")
class flagIndex(flagrPage):
        def GET(self):
                """
                """
                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                        {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                        ("original-title", "Quick select")],
                                rel="tooltip"))

                if c.session.loggedIn:
                        self.view["title"] = "Your Flags"

                        flags = fm.flagList(c.session.userID, True)
                        pageHead = new

                        pageHead = ps.baseRow([ps.baseColumn(ps.baseHeading("%s Your flags" % (ps.baseIcon("flag")), size=1)), ps.baseColumn(pageHead, classes="pull-right")])


                        buildMessage = "You have no flags at the moment, but if you want to add one, simply click the button up above to get started!."

                        if flags:
                                width=10
                                flagList = fc.flagThumbnails(flags, width)

                                flagList = ps.baseUL(flagList, classes="thumbnails")
                        else:
                                flagList = buildMessage

                        self.view.body = pageHead + "<hr>" + ps.baseRow(ps.baseColumn(flagList, id="flags"))
                        self.view.scripts = ps.baseScript("""
                        $('.btn-group').tooltip({
                              selector: "a[rel=tooltip]"
                        })
        """)
                else:
                        self.head = ("303 SEE OTHER", [("location", str("/public"))])
                        c.session.pushMessage(("You're not logged in, so we've sent you here to see some of the pretty public flags!"), icon="exclamation-sign", title="Oh snap!!")


@route("/flag/(.*)/edit")
@route("/flags/edit/(.*)")
class newFlag(flagrPage):
        __login__ = True
        def GET(self):
                flag = fm.flag(self.members[0])
                if flag["userID"] != c.session.userID:
                        self.head = ("303 SEE OTHER", [("location", str("/flag/%s/copy"%flag.id))])
                        c.session.pushMessage(("You didn't create the flag: %s, but we can allow you to make a copy of it!" % ps.baseBold(flag.title)), type="error", icon="fire", title="Oh no!")
                        return


                self.view.title = "Editing flag: %s" % flag.title

                labels = ", ".join(flag["labels"])

                elements = [
                ps.baseInput(type="text", classes="span10", name="title", value=flag["title"], placeholder="Title"),
                "<br /><br />",
                {"content": ps.baseTextarea(classes="span10", name="description", content=flag["description"]),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                ps.baseInput(type="text", classes="span10", name="labels", value=labels, placeholder="Labels"),
                "<br /><br />",
                {"label": "Make it public?",
                        "content": ps.baseCheckbox(name="visibility", checked=flag["visibility"],
                        label="If you want the rest of the world to be able to see this flag, mark the checkbox. If not, leave it unchecked.")},
                        ]

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                name = field[0].lower() if type(field) != str else field.lower()
                                elements.append(ps.baseInput(type="text", classes="span10", name=name, value=flag[field], placeholder=name.title()))


                editForm = ps.baseHeading("%s Editing flag: %s" % (ps.baseIcon(flag.icon), flag["title"]), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/flag/%s/edit"% (self.members[0]),
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Update!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                flag = fm.flag(self.members[0])
                if flag["userID"] != c.session.userID:
                        self.head = ("303 SEE OTHER", [("location", str("/flag/#s/copy"%flag.id))])
                        c.session.pushMessage(("You didn't create the flag: %s, but we can allow you to make a copy of it!" % ps.baseBold(flag.title)), type="error", icon="fire", title="Oh no!")
                        return

                if self.members.has_key("labels"):
                        self.members["labels"] = { unicode(i) for i in self.members["labels"].replace(" ", "").split(",") }

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in flag.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                flag[part] = self.members[part]

                flag.commit()
                self.head = ("303 SEE OTHER", [("location", str("/flag/%s"%flag.id))])
                c.session.pushMessage(("You updated flag: %s!" % ps.baseBold(flag.title)), type="success", icon="ok", title="YAY!")


@route("/flags/new")
class newFlagChoice(flagrPage):
        __menu__ = "Make a new Flag"
        __login__ = True
        def GET(self):
                """
                """
                newSelect = []
                types = [{"type": "bookmark", "title": "%s Bookmark Flag" % ps.baseIcon("bookmark"),
                                "description": "A useful tool for making rounds on the internet and saving the pages you want."},
                        {"type": "note", "title": "%s Note Flag" % ps.baseIcon("list-alt"),
                                "description": "Just a general flag designed more taking quick notes or writing long essays."}]

                for flag in types:
                        flag["description"] += "<br /><br />" + ps.baseAButton(ps.baseIcon("flag")+" I want this one!", link=c.baseURL+"/flags/new/"+flag["type"], classes="btn-info")
                        newSelect.append(ps.baseTextThumbnail(label=flag["title"], caption=flag["description"], width=5))

                self.view.body = ps.baseHeading("%s Take your preference..." % ps.baseIcon("flag"), size=1) + ps.baseUL(newSelect, classes="thumbnails")


@route("/flags/new/(.*)")
class newFlag(flagrPage):
        __login__ = True
        __menu__ = "Make a New Flag"
        def GET(self):
                flag = fm.flag(flagType=self.members[0])

                self.view.title = "Making a new flag"

                elements = [
                ps.baseInput(type="text", classes="span10", name="title", placeholder="Title"),
                "<br /><br />",
                {"content": ps.baseTextarea(classes="span10", name="description"),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                ps.baseInput(type="text", classes="span10", name="labels", placeholder="Labels"),
                "<br /><br />",
                {"label": "Make it public?",
                        "content": ps.baseCheckbox(name="visibility",
                        label="If you want the rest of the world to be able to see this flag, mark the checkbox. If not, leave it unchecked.")},
                        ]

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                name = field[0].lower() if type(field) != str else field.lower()
                                elements.append(ps.baseInput(type="text", classes="span10", name=name, placeholder=name.title()))



                editForm = ps.baseHeading("%s Make a new %s flag" % (ps.baseIcon(flag.icon), flag["flagType"]), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/flags/new/%s"% (self.members[0]),
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Create!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                flag = fm.flag(flagType=self.members[0])
                if self.members.has_key("labels"):
                        self.members["labels"] = { unicode(i) for i in self.members["labels"].replace(" ", "").split(",") }
                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in flag.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                flag[part] = self.members[part]

                flag.commit()
                self.head = ("303 SEE OTHER", [("location", str("/flag/%s"%flag.id))])
                c.session.pushMessage(("You created flag: %s!" % ps.baseBold(flag.title)), type="success", icon="ok", title="YAY!")


@route("/flag/(.*)/delete")
@route("/flags/delete/(.*)")
class deleteFlag(flagrPage):
        __login__ = True
        def GET(self):
                id = self.members[0]
                flag = fm.flag(id)
                if flag["userID"] != c.session.userID:
                        self.head = ("303 SEE OTHER", [("location", str("/flags"))])
                        c.session.pushMessage("You didn't create the flag: %s, so we can't allow you to delete it. Sorry!", type="error", icon="fire", title="Oh no!")
                        return

                self.view.title = "Delete flag %s" % flag.title

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete your flag: %s"% flag.title , classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this flag forever and you will not be able to recover it. Are you sure you would like to continue?", classes="text-warning")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/flag/%s/delete"%flag.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("Yes, Delete it.", classes="btn-danger"), ps.baseAButton("NO, Do Not Delete!", link=c.baseURL+"/flags/edit/"+flag.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=confirm

        def POST(self):
                id = self.members[0]
                flag = fm.flag(id)

                if flag["userID"] != c.session.userID:
                        self.head = ("303 SEE OTHER", [("location", str("/flags"))])
                        c.session.pushMessage(("You didn't create the flag: %s, so we can't allow you to delete it. Sorry!" % ps.baseBold(flag.title)), type="error", icon="fire", title="Oh snap!")
                        return

                flag.delete()

                self.head = ("303 SEE OTHER", [("location", "/flags")])
                c.session.pushMessage(("The flag %s was deleted" % ps.baseBold(flag.title)), type="error")


@route("/flag/(.*)/copy")
@route("/flags/copy/(.*)")
class copyFlag(flagrPage):
        __login__ = True
        def GET(self):
                flag = fm.flag(self.members[0])

                self.view.title = "Copying flag: %s" % flag.title

                labels = ", ".join(flag["labels"])

                elements = [
                ps.baseInput(type="text", classes="span10", name="title", value=flag["title"], placeholder="Title"),
                "<br /><br />",
                {"content": ps.baseTextarea(classes="span10", name="description", content=flag["description"]),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                ps.baseInput(type="text", classes="span10", name="labels", value=labels, placeholder="Labels"),
                "<br /><br />",
                {"label": "Make it public?",
                        "content": ps.baseCheckbox(name="visibility", checked=flag["visibility"],
                        label="If you want the rest of the world to be able to see this flag, mark the checkbox. If not, leave it unchecked.")},
                ps.baseInput(type="hidden", value=flag["flagType"], name="flagType"),
                ps.baseInput(type="hidden", value=flag["title"], name="oldTitle"),
                        ]

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                name = field[0].lower() if type(field) != str else field.lower()
                                elements.append(ps.baseInput(type="text", classes="span10", name=name, value=flag[field], placeholder=name.title()))


                editForm = ps.baseHeading("%s Copying flag: %s" % (ps.baseIcon(flag.icon), flag["title"]), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/flag/%s/copy"% (self.members[0]),
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Copy!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                flag = fm.flag(flagType=self.members["flagType"])

                if self.members.has_key("labels"):
                        self.members["labels"] = { unicode(i) for i in self.members["labels"].replace(" ", "").split(",") }

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in flag.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                flag[part] = self.members[part]

                flag.commit()
                self.head = ("303 SEE OTHER", [("location", str("/flag/%s"%flag.id))])
                c.session.pushMessage("You made a copy of flag: %s called %s!" % (ps.baseBold(self.members["oldTitle"]), ps.baseBold(flag["title"])), type="success", icon="ok", title="YAY!")


@route("/flag/(.*)")
@route("/flag/(.*)/view")
@route("/flags/view/(.*)")
class viewFlag(flagrPage):
        def GET(self):
                """
                """
                flagID = self.members[0]

                flag = fm.flag(flagID, md=True)

                if not flag.visibility and flag.userID != c.session.userID:
                        content = ps.baseHeading("Oh no!", size=2)
                        content += ps.baseParagraph("This flag isn't public, and your either not logged in, or not the owner of the flag!")

                else:
                        self.view["title"] = "Viewing flag: %s" % (flag.title)
                        content = ""

                        if c.session.loggedIn and c.session.userID == flag["userID"]:
                                edit = ps.baseColumn(
                                        ps.baseButtonGroup([
                                                ps.baseAButton("%s" % ps.baseIcon("copy"),
                                                        link=c.baseURL+"/flag/%s/copy"%flag.id,
                                                        classes="", rel="tooltip", data=[("original-title", "Copy Flag")]),
                                                ps.baseAButton("%s" % ps.baseIcon("edit"),
                                                        link=c.baseURL+"/flag/%s/edit"%flag.id,
                                                        classes="btn-info ", rel="tooltip", data=[("original-title", "Edit Flag")]),
                                                ps.baseAButton("%s" % ps.baseIcon("trash"),
                                                        link=c.baseURL+"/flag/%s/delete"%flag.id,
                                                        classes="btn-danger ", rel="tooltip", data=[("original-title", "Delete Flag")])
                                        ])
                                 )
                        elif c.session.loggedIn and c.session.userID != flag["userID"]:
                                edit = ps.baseColumn(
                                        ps.baseButtonGroup([
                                                ps.baseAButton("%s" % ps.baseIcon("copy"),
                                                        link=c.baseURL+"/flag/%s/copy"%flag.id,
                                                        classes="", rel="tooltip", data=[("original-title", "Copy Flag")])
                                                ])
                                 )
                        else:
                                edit = ""

                        content += ps.baseHeading("%s %s" % (ps.baseIcon(flag.icon), flag.title), size=1, classes="")

                        if flag["userID"] == c.session.userID:
                                author = "You"
                        else:
                                author = flag.author

                        if flag["visibility"]:
                                vis = "%s Public" % ps.baseIcon("globe")
                        else:
                                vis = "%s Private" % ps.baseIcon("eye-close")

                        content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted")) +
                                        ps.baseColumn(author) + 
                                        ps.baseColumn(ps.baseBold("When: ", classes="muted")) +
                                        ps.baseColumn(flag.time) + 
                                        ps.baseColumn(vis) + 
                                        ps.baseColumn(edit, classes="pull-right")
                                ), width=10
                        ))

                        content += ps.baseRow(ps.baseColumn(flag.description))

                        for field in flag.fields:
                                name = field[0] if type(field) != str else field
                                if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                        if name in ["url"]:
                                                d = flag[name]
                                                value = ps.baseAnchor(d, link=d)
                                        else:
                                                value = flag[name]
                                        content += ps.baseRow(ps.baseColumn("%s: %s" %(ps.baseBold(name.lower().title(), classes="muted"), value)))

                        if not flag["visibility"]:
                                other = ps.baseLabel("%s Private" % ps.baseIcon("eye-close"))
                        else:
                                other = ps.baseAnchor(ps.baseLabel("%s Public" % ps.baseIcon("globe")), link=c.baseURL+"/public")

                        labelLinks = "%s " % other
                        for label in flag["labels"]:
                                labelLinks += ps.baseAnchor(ps.baseLabel(label, classes="label-info"), link=c.baseURL+"/label/%s"%label) + " "

                        content += ps.baseRow([
                                ps.baseColumn(ps.baseBold("Labels: ", classes="muted"), width=1),
                                ps.baseColumn(labelLinks, width=7)
                                ])


                self.view.body = content
                self.view.scripts = ps.baseScript("""
                $('.btn-group').tooltip({
                      selector: "a[rel=tooltip]"
                })
""")

