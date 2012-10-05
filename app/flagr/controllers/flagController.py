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


@route("/flags")
class flagIndex(flagrPage):
        def GET(self):
                """
                """

                if self.members.has_key("view"): view = self.members["view"]
                else: view = ""

                if c.session.loggedIn == "True":
                        self.view["title"] = "Your Flags"
                        flags = fm.flagList(c.session.userID, True)
                        if flags:
                                pageHead = ps.baseButtonToolbar([
                                        ps.baseButtonGroup([
                                                ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                                                        classes="btn-info", link=c.baseURL + "/flags/new", data=[("title", "New Flag"),("original-title", "New Flag")], rel="tooltip", title="New Flag")
                                        ]), ps.baseButtonGroup([
                                                ps.baseAButton(ps.baseIcon("th"),
                                                        link=c.baseURL+"/flags?view=cards", data=[("original-title", "View as cards")], rel="tooltip"),
                                                ps.baseAButton(ps.baseIcon("list"),
                                                        link=c.baseURL+"/flags", data=[("original-title", "View as list")], rel="tooltip")
                                                ], classes="pull-right")
                                        ]) + "<hr>"
                        else:
                                pageHead = ps.baseButtonToolbar([
                                        ps.baseButtonGroup([
                                                ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                                                        classes="btn-info", link=c.baseURL + "/flags/new", data=[("title", "New Flag"),("original-title", "New Flag")], rel="tooltip", title="New Flag")
                                        ])
                                        ]) + "<hr>"


                        buildMessage = "You have no flags at the moment, but if you want to add one, simply click the button up above to get started!."

                else:
                        flags = fm.flagList(md=True)
                        self.view["title"] = "Public Flags"
                        if flags:
                                pageHead = ps.baseButtonToolbar([
                                        ps.baseButtonGroup([
                                                ps.baseAButton(ps.baseIcon("th"),
                                                        link=c.baseURL+"/flags?view=cards", data=[("original-title", "View as cards")], rel="tooltip"),
                                                ps.baseAButton(ps.baseIcon("list"),
                                                        link=c.baseURL+"/flags", data=[("original-title", "View as list")], rel="tooltip")
                                                ], classes="pull-right")
                                        ]) + "<br /><hr>"
                        else:
                                pageHead = ""

                        buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags just yet! If you'd like to make your own flags, please login."

                if flags:
                        flagList = ""
                        for flag in flags:
                                title = ps.baseIcon(flag.icon) +  " %s" % flag.title

                                if not flag["visibility"]:
                                        other = ps.baseAButton("%s Private" % ps.baseIcon("eye-close"))
                                else:
                                        other = ps.baseAButton("%s Public" % ps.baseIcon("globe"))

                                caption = "%s%s<br />" % (flag["description"][:250], ps.baseAnchor("...", link=c.baseURL+"/flags/view/"+flag.id))

                                for field in flag.fields:
                                        name = field[0] if type(field) != str else field
                                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                                if name in ["url"]:
                                                        d = flag[name]
                                                        value = ps.baseAnchor(d, link=d)
                                                else:
                                                        value = flag[name]
                                                caption += "%s: %s" %(name.lower().title(), value)

                                if c.session.loggedIn == "True":
                                        caption += ps.baseButtonToolbar([
                                                ps.baseButtonGroup([
                                                        ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                                link=c.baseURL+"/flags/view/"+flag.id, classes="", rel="Expand"),
                                                        ps.baseAButton("%s" % ps.baseIcon("edit"),
                                                                link=c.baseURL+"/flags/edit/"+flag.id, classes="btn-info", rel="Edit"),
                                                        ps.baseAButton("%s" % ps.baseIcon("trash"),
                                                                link=c.baseURL+"/flags/delete/"+flag.id, classes="btn-danger", rel="Delete")]),
                                                other])
                                else:
                                        caption +="<br />" +  ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                                                link=c.baseURL+"/flags/view/"+flag.id,
                                                                classes="",
                                                                rel="Expand")

                                labelLinks = ""
                                for label in flag["labels"]:
                                        labelLinks += ps.baseAnchor(ps.baseLabel(label, classes="label-info"), link=c.baseURL+"/labels/view/"+label) + " "

                                caption += ps.baseRow([
                                        ps.baseColumn(ps.baseBold("Labels: ", classes="muted"), width=1),
                                        ps.baseColumn(labelLinks)
                                        ])


                                if view == "cards":
                                        flagList += ps.baseTextThumbnail(label=title, caption=caption, classes="span4")
                                else:
                                        flagList += ps.baseTextThumbnail(label=title, caption=caption, classes="span8")

                        flagList = ps.baseUL(flagList, classes="thumbnails")
                else:
                        flagList = buildMessage

                self.view.body = pageHead + flagList


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

                        if c.session.loggedIn == "True":
                                content += ps.baseButtonToolbar([
                                        ps.baseButtonGroup([
                                                ps.baseAButton("%s" % ps.baseIcon("edit"),
                                                        link=c.baseURL+"/flags/edit/"+flag.id, classes="btn-info", rel="Edit"),
                                                ps.baseAButton("%s" % ps.baseIcon("trash"),
                                                        link=c.baseURL+"/flags/delete/"+flag.id, classes="btn-danger", rel="Delete")]),
                                        ps.baseAButton("%s Copy" % ps.baseIcon("copy"), link=c.baseURL+"/flags/copy/"+flag.id)])

                        content += ps.baseHeading("%s %s" % (ps.baseIcon(flag.icon), flag.title), size=1)

                        if flag.userID == c.session.userID:
                                author = "You"
                        else:
                                author = flag.author

                        if flag["visibility"]:
                                vis = "%s Public" % ps.baseIcon("globe")
                        else:
                                vis = "%s Private" % ps.baseIcon("eye-close")

                        content += ps.baseRow(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted")) +
                                        ps.baseColumn(author) + 
                                        ps.baseColumn(ps.baseBold("When: ", classes="muted")) +
                                        ps.baseColumn(flag.time) + 
                                        ps.baseColumn(vis)
                                )
                        )

                        content += ps.baseRow(flag.description)

                        for field in flag.fields:
                                name = field[0] if type(field) != str else field
                                if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                        if name in ["url"]:
                                                d = flag[name]
                                                value = ps.baseAnchor(d, link=d)
                                        else:
                                                value = flag[name]
                                        content += ps.baseRow("%s: %s" %(name.lower().title(), value))

                        labelLinks = ""
                        for label in flag["labels"]:
                                labelLinks += ps.baseAnchor(ps.baseLabel(label, classes="label-info"), link=c.baseURL+"/labels/view/"+label) + " "

                        content += ps.baseRow([
                                ps.baseColumn(ps.baseBold("Labels: ", classes="muted"), width=1),
                                ps.baseColumn(labelLinks, width=7)
                                ])


                self.view.body = content


@route("/flags/edit/(.*)")
class newFlag(flagrPage):
        __login__ = "True"
        def GET(self):
                flag = fm.flag(self.members[0])

                self.view.title = "Editing flag: %s" % flag.title

                labels = ", ".join(flag["labels"])

                elements = []
                elements.append({"label": "Title",
                        "content": ps.baseInput(type="text", classes="span5", name="title", value=flag["title"])})
                elements.append({"label": "Labels",
                        "content": ps.baseInput(type="text", classes="span5", name="labels", value=labels)})
                elements.append({"label": "Make it public?",
                        "content": ps.baseCheckbox(name="visibility", checked=flag["visibility"])})
                elements.append({"label": "Description",
                        "content": ps.baseTextarea(classes="span5", name="description", content=flag["description"])})

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                name = field[0].lower() if type(field) != str else field.lower()
                                elements.append({"label": name.title(),
                                        "content": ps.baseInput(type="text", classes="span5", name=name, value=flag[field])})


                editForm = ps.baseHorizontalForm(action=c.baseURL+"/flags/edit/%s"% (self.members[0]),
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Update!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                flag = fm.flag(self.members[0])
                if self.members.has_key("labels"):
                        self.members["labels"] = { unicode(i) for i in self.members["labels"].replace(" ", "").split(",") }

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in flag.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                flag[part] = self.members[part]

                flag.commit()
                self.head = ("303 SEE OTHER", [("location", str("/flags/view/"+flag.id))])
                c.session.pushMessage(("You updated flag: %s!" % ps.baseBold(flag.title)), type="success", icon="ok", title="YAY!")


@route("/flags/new")
class newFlagChoice(flagrPage):
        __menu__ = "Make a new Flag"
        __login__ = "True"
        def GET(self):
                """
                """
                newSelect = []
                types = [{"type": "bookmark", "title": "%s Bookmark" % ps.baseIcon("bookmark"),
                                "description": "A useful tool for making the rounds on the internet and saving the pages you want."},
                        {"type": "note", "title": "%s Note" % ps.baseIcon("list-alt"),
                                "description": "General note Flag, this is a versitile little Flag with a lot of potential!"}]

                for flag in types:
                        flag["description"] += "<br /><br />" + ps.baseAButton(ps.baseIcon("flag")+" I want this one!", link=c.baseURL+"/flags/new/"+flag["type"], classes="btn-info")
                        newSelect.append(ps.baseTextThumbnail(label=flag["title"], caption=flag["description"], width=4))

                self.view.body = ps.baseUL(newSelect, classes="thumbnails")


@route("/flags/new/(.*)")
class newFlag(flagrPage):
        __login__ = "True"
        __menu__ = "Make a New Flag"
        def GET(self):
                flag = fm.flag(flagType=self.members[0])

                self.view.title = "Making a new flag"

                elements = []
                elements.append({"label": "Title",
                        "content": ps.baseInput(type="text", classes="span5", name="title", placeholder="Title")})
                elements.append({"label": "Labels",
                        "content": ps.baseInput(type="text", classes="span5", name="labels", placeholder="Labels")})
                elements.append({"label": "Make it public?",
                        "content": ps.baseCheckbox(name="visibility")})
                elements.append({"label": "Description",
                        "content": ps.baseTextarea(classes="span5", name="description")})

                for field in flag.fields:
                        name = field[0] if type(field) != str else field
                        if name not in ["title", "description", "labels", "time", "visibility", "author", "userID", "flagType"]:
                                name = field[0].lower() if type(field) != str else field.lower()
                                elements.append({"label": name.title(),
                                        "content": ps.baseInput(type="text", classes="span5", name=name, placeholder=field.title())})


                editForm = ps.baseHorizontalForm(action=c.baseURL+"/flags/new/%s"% (self.members[0]),
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
                self.head = ("303 SEE OTHER", [("location", str("/flags/view/"+flag.id))])
                c.session.pushMessage(("You created flag: %s!" % ps.baseBold(flag.title)), type="success", icon="ok", title="YAY!")


@route("/flags/delete/(.*)")
class deleteFlag(flagrPage):
        __login__ = "True"
        def GET(self):
                id = self.members[0]
                flag = fm.flag(id)

                self.view.title = "Delete flag %s" % flag.title

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete your flag: %s"% flag.title , classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this flag forever and you will not be able to recover it. Are you sure you would like to continue?", classes="text-warning")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/flags/delete/"+flag.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("Yes, Delete it.", classes="btn-danger"), ps.baseAButton("NO, Do Not Delete!", link=c.baseURL+"/flags/edit/"+flag.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=confirm

        def POST(self):
                id = self.members[0]
                flag = fm.flag(id)

                flag.delete()

                self.head = ("303 SEE OTHER", [("location", "/flags")])
                c.session.pushMessage(("The flag %s was deleted" % ps.baseBold(flag.title)), type="error")

'''
@route("/flags/copy/(.*)")
class copyFlag(basePage):
        __login__ == "True"
        def GET(self):

        def POST(self):



@route("/flags/random")
class randomFlag(basePage):
        def GET(self):
                """
                """
                flags = fm.randomFlagList()

                elements = fe.flagElements()
                if c.session.loggedIn == "True":
                        view = bv.sidebarView()
                        view["sidebar"] = elements.sidebar()

                        view["title"] = "Random Flags"

                        buildMessage = "OH NO! I couldn't find you any random publically visibile flags to display!"

                        offset = 0

                else:
                        view = bv.noSidebarView()

                        view["title"] = "Random Flags"

                        buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags just yet! If you'd like to make your own flags, please login."

                        offset = 2

                view["nav"] = elements.navbar()

                view["messages"] = bv.baseRow(c.session.getMessages(), 12, 0)

                flagList = bl.baseList(flags, "row_list_flag", message=buildMessage)

                view["content"] = bv.baseRow(flagList, 8, offset=offset)

                return view.build()


@route("/flags/user/(.*)")
class userFlag(basePage):
        def GET(self):
                """
                """
                userID = self.members[0]
                flags = fm.userFlagList(userID)

                user = am.baseUser(userID)

                elements = fe.flagElements()
                if c.session.loggedIn == "True":
                        view = bv.sidebarView()
                        view["sidebar"] = elements.sidebar()

                        view["title"] = "User %s's Flags" % user.username

                        buildMessage = "OH NO! I couldn't find you any publically visibile flags from this user to display!"

                        offset = 0

                else:
                        view = bv.noSidebarView()

                        view["title"] = "User %s's Flags" % user.username

                        buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags for this user just yet! If you'd like to make your own flags, please login."

                        offset = 2

                view["nav"] = elements.navbar()

                view["messages"] = bv.baseRow(c.session.getMessages(), 12, 0)

                flagList = bl.baseList(flags, "row_list_flag", message=buildMessage)

                view["content"] = bv.baseRow(flagList, 8, offset=offset)

                return view.build()
'''
