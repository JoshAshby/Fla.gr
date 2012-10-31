#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
controller for authentication stuff.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from flagr.objects.adminObject import adminObject
from seshat.route import route

import flagr.models.carouselModel as cm
import flagr.views.pyStrap.pyStrap as ps


@route("/admin/carousels")
class carouselIndex_admin(adminObject):
        def GET(self):
                """
                """
                carousel = cm.carouselList(md=True)

                hero = ""

                if carousel:
                        carouselList = [ ps.baseColumn(item["content"], offset=1, width=6) for item in carousel if item["visibility"] ]

                        if carouselList: hero = ps.baseHero(ps.baseCarousel(items=carouselList, id="frontCarousel"))

                self.view["title"] = "Carousel"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Front page carousel" % ps.baseIcon("play"), size=1)),
                                ps.baseButtonGroup([
                                        ps.baseAButton(ps.baseIcon("magic"), link=c.baseURL+"/admin/carousels/new",
                                        data=[("original-title", "New Item")],
                                        rel="tooltip",
                                        classes="btn-info"),
                                        ps.baseAButton(ps.baseIcon("wrench"),
                                                link=c.baseURL+"/admin/carousels/drafts",
                                                data=[("original-title", "View Drafts")],
                                                rel="tooltip",
                                                classes="")

                                        ], classes="pull-right")
                        ]) + "<hr>"


                if carousel:
                        content = ""
                        for carouselItem in carousel:
                                if not carouselItem["visibility"]:
                                        other = ps.baseAnchor(ps.baseLabel("%s Draft" % ps.baseIcon("eye-close")), link=c.baseURL+"/admin/carousels/drafts")
                                else:
                                        other = ps.baseLabel("%s Published" % ps.baseIcon("globe"))
  
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph(carouselItem["content"][:50]+ps.baseAnchor("...", link=c.baseURL+"/admin/carousel/"+carouselItem.id))),
                                        ])

                                edit = ps.baseSplitDropdown(btn=ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                        classes="", link=c.baseURL+"/admin/carousel/%s"%carouselItem.id,
                                        rel="tooltip",
                                        data=[("original-title", "Expand")]),
                                        dropdown=ps.baseMenu(name="postDropdown",
                                                items=[{"name": "%s Edit" % ps.baseIcon("edit"), "link": c.baseURL+"/admin/carousel/%s/edit"%carouselItem.id},
                                                        {"name": ps.baseBold("%s Delete" % ps.baseIcon("trash"), classes="text-error"), "link": c.baseURL+"/admin/carousel/%s/delete"%carouselItem.id}]
                                                ),
                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                classes="dropdown-toggle btn-danger",
                                                data=[("toggle", "dropdown"),
                                                        ("original-title", "Edit Options")],
                                                rel="tooltip"))

                                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                                        ps.baseColumn(carouselItem.author)+
                                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                                        ps.baseColumn(carouselItem.time)+
                                        ps.baseColumn(other)+
                                        ps.baseColumn(edit, classes="pull-right")
                                        ), width=8
                                ))
                                content += "<hr>"
                else:
                        content = "You don't have any carousel items! Why don't you make one?"

                self.view["body"] = pageHead + hero + content


@route("/admin/carousels/drafts")
class carouselDrafts_admin(adminObject):
        def GET(self):
                """
                """
                carousel = cm.carouselList(md=True)

                self.view["title"] = "Carousel drafts"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Front page carousel: Drafts" % ps.baseIcon("play"), size=1)),
                                ps.baseButtonGroup([
                                        ps.baseAButton(ps.baseIcon("magic"), link=c.baseURL+"/admin/carousels/new",
                                        data=[("original-title", "New Item")],
                                        rel="tooltip",
                                        classes="btn-info"),
                                        ps.baseAButton(ps.baseIcon("wrench"),
                                                link=c.baseURL+"/admin/carousels",
                                                data=[("original-title", "View All")],
                                                rel="tooltip",
                                                classes="")

                                        ], classes="pull-right")
                        ]) + "<hr>"


                content = ""
                for carouselItem in carousel:
                        if not carouselItem["visibility"]:
                                other = ps.baseAnchor(ps.baseLabel("%s Draft" % ps.baseIcon("eye-close")), link=c.baseURL+"/admin/carousels/drafts")
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph(carouselItem["content"][:50]+ps.baseAnchor("...", link=c.baseURL+"/admin/carousel/%s"%carouselItem.id))),
                                        ])
                                edit = ps.baseSplitDropdown(btn=ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                        classes="", link=c.baseURL+"/admin/carousel/%s"%carouselItem.id,
                                        rel="tooltip",
                                        data=[("original-title", "Expand")]),
                                        dropdown=ps.baseMenu(name="postDropdown",
                                                items=[{"name": "%s Edit" % ps.baseIcon("edit"), "link": c.baseURL+"/admin/carousel/%s/edit"%carouselItem.id},
                                                        {"name": ps.baseBold("%s Delete" % ps.baseIcon("trash"), classes="text-error"), "link": c.baseURL+"/admin/carousel/%s/delete"%carouselItem.id}]
                                                ),
                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                classes="dropdown-toggle btn-danger",
                                                data=[("toggle", "dropdown"),
                                                        ("original-title", "Edit Options")],
                                                rel="tooltip"))

                                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                                        ps.baseColumn(carouselItem.author)+
                                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                                        ps.baseColumn(carouselItem.time)+
                                        ps.baseColumn(other)+
                                        ps.baseColumn(edit, classes="pull-right")
                                        ), width=8
                                ))
                                content += "<hr>"
                if not content:
                        content = "You don't have any draft carousel items! Why don't you make one?"

                self.view["body"] = pageHead + content


@route("/admin/carousel/(.*)/edit")
class carouselEdit_admin(adminObject):
        def GET(self):
                carouselItem = cm.carousel(self.members[0])

                self.view.title = "Editing Carousel: %s" % carouselItem.id

                elements = [
                {"content": ps.baseTextarea(classes="span8", name="content", content=carouselItem["content"]),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                {"label": "Publish?",
                        "content": ps.baseCheckbox(name="visibility", checked=carouselItem["visibility"],
                        label="If you want the rest of the world to be able to see this carousel item, mark the checkbox. If not, leave it unchecked to mark as a draft.")},
                        ]


                editForm = ps.baseHeading("%s Editing Carousel: %s" % (ps.baseIcon("play"), carouselItem.id), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/admin/carousel/%s/edit"% (self.members[0]),
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Update!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                carouselItem = cm.carousel(self.members[0])

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in carouselItem.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                carouselItem[part] = self.members[part]

                carouselItem.commit()
                self.head = ("303 SEE OTHER", [("location", str("/admin/carousel/"+carouselItem.id))])
                c.session.pushAlert(("You updated the carousel item: %s!" % ps.baseBold(carouselItem.id)), type="success", icon="ok", title="YAY!")


@route("/admin/carousel/(.*)/delete")
class carouselDelete_admin(adminObject):
        def GET(self):
                id = self.members[0]
                carouselItem = cm.carousel(id)

                self.view.title = "Delete Carousel Item: %s" % carouselItem.id

                confirm = ps.baseHeading("%s Delete Carousel: %s" % (ps.baseIcon("play"), carouselItem.id), size=1, classes="text-error")

                confirm += ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete the carousel item: %s" % carouselItem.id, classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this carousel item forever and you will not be able to recover it. Are you sure you would like to continue?")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/admin/carousel/%s/delete"%carouselItem.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("Yes, I am sure.", classes="btn-danger"), ps.baseAButton("NO, Do Not Delete!", link=c.baseURL+"/admin/carousel/%s/edit"%carouselItem.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=confirm

        def POST(self):
                id = self.members[0]
                carouselItem = cm.carousel(id)

                carouselItem.delete()

                self.head = ("303 SEE OTHER", [("location", "/admin/carousel")])
                c.session.pushAlert(("The carousel item %s was deleted" % ps.baseBold(carouselItem.id)), title="Bye Bye", icon="trash", type="error")


@route("/admin/carousels/new")
class carouselNew_admin(adminObject):
        def GET(self):
                self.view.title = "Creating a new carousel item"
                title = ps.baseHeading("%s Creating a new carousel..." % (ps.baseIcon("play")), size=1)

                elements = [
                {"content": ps.baseTextarea(classes="span8", name="content"),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                {"label": "Publish?",
                        "content": ps.baseCheckbox(name="visibility",
                        label="If you want the rest of the world to be able to see this carousel, mark the checkbox. If not, leave it unchecked to mark as a draft.")},
                        ]


                editForm = ps.baseHeading("%s Creating a new carousel" % (ps.baseIcon("play")), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/admin/carousel/new",
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Create!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                carouselItem = cm.carousel()

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in carouselItem.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                carouselItem[part] = self.members[part]

                carouselItem.commit()
                self.head = ("303 SEE OTHER", [("location", str("/admin/carousel/"+carouselItem.id))])
                c.session.pushAlert(("You created carousel item: %s!" % ps.baseBold(carouselItem.id)), type="success", icon="ok", title="YAY!")


@route("/admin/carousel/(.*)")
class carouselView_admin(adminObject):
        def GET(self):
                """
                """
                carouselItem = cm.carousel(self.members[0], True)

                self.view["title"] = "Carousel: %s" % carouselItem.id
                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Viewing carousel item: %s" % (ps.baseIcon("play"), carouselItem.id), size=1))
                        ]) + "<hr>"

                content = ""

                if not carouselItem["visibility"]:
                        other = ps.baseAnchor(ps.baseLabel("%s Draft" % ps.baseIcon("eye-close")), link=c.baseURL+"/admin/carousel/drafts")
                else:
                        other = ps.baseLabel("%s Published" % ps.baseIcon("globe"))

                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                        ps.baseColumn(carouselItem.author)+
                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                        ps.baseColumn(carouselItem.time)+
                        ps.baseColumn(other)+
                        ps.baseColumn(
                                ps.baseButtonGroup([
                                ps.baseAButton(ps.baseIcon("edit"),
                                        classes="btn-info",
                                        link=c.baseURL+"/admin/carousel/%s/edit"%carouselItem.id,
                                        data=[("original-title", "Edit Item")],
                                        rel="tooltip"),
                                ps.baseAButton(ps.baseIcon("trash"),
                                        classes="btn-danger",
                                        link=c.baseURL+"/admin/carousel/%s/delete"%carouselItem.id,
                                        data=[("original-title", "Delete Item")],
                                        rel="tooltip")
                                        ]), classes="pull-right"
                                )
                        ), width=8
                ))

                content += ps.baseRow([
                        ps.baseColumn(ps.baseHero(carouselItem["content"])),
                        ])

                self.view["body"] = pageHead + content
