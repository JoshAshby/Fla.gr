#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
base HTML page template

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import flagr.views.pyStrap.pyStrap as ps
import seshat.baseView as bv


class smartView(object):
        """
        basePage

        Abstract:
                Very base page for flagr

        Accepts:
                title
                navbar
                header
                sidebar
                body
                footer
                fluid


        Returns:
                str - String of HTML which represents a HTML page

        """
        __defaultParts__ = [ "title", "navbar", "header", "sidebar", "body", "footer", "page", "alerts", "fluid", "scripts", "css", "tabbar"]
        def __init__(self, **kwargs):
                for part in self.__defaultParts__:
                        setattr(self, part, "")

                for kwarg in kwargs:
                        setattr(self, kwarg, kwargs[kwarg])

                self.finishInit()

        def finishInit(self):
                pass

        def __repr__(self):
                return self.page

        def __str__(self):
                return str(self.page)

        def __unicode__(self):
                return u"%s" % self.page

        def __add__(self, other):
                return str(self.page) + other

        def __radd__(self, other):
                return other + str(self.page)

        def __getattr__(self, item):
                return object.__getattribute__(self, item)

        def __getitem__(self, item):
                return object.__getattribute__(self, item)

        def __setattr__(self, item, value):
                return object.__setattr__(self, item, value)

        def __setitem__(self, item, value):
                return object.__setattr__(self, item, value)

        def build(self):
                if self.fluid:
                        fluid = "-fluid"
                else: fluid = ""

                content = ""

                if self.navbar: content += self.navbar
                if self.header: content += """
                <div id="header">
                        <div class="container">
                                %s
                        </div>
                </div>
                """ % ps.baseRow(columns=[self.header])

                content += """
                <div style="padding: 20px">
                        <div class="container%s">
                """ % fluid

                if c.session.alerts:
                        self.alerts = ps.baseRow(ps.baseColumn(c.session.alerts, width=10, offset=1))

                content += self.alerts

                if self.sidebar and self.tabbar:
                        self.sidebar = ps.baseColumn(self.sidebar, width=3)
                        self.body = ps.baseColumn(self.body, width=9)
                        row = ps.baseRow([self.sidebar, self.body])
                elif self.sidebar:
                        self.sidebar = ps.baseColumn(self.sidebar, width=4)
                        self.body = ps.baseColumn(self.body, width=8)
                        row = ps.baseRow([self.sidebar, self.body])
                elif self.tabbar:
                        self.body = ps.baseColumn(self.body, width=11, offset=1)
                        row = ps.baseRow(self.body)
                else:
                        self.body = ps.baseColumn(self.body, width=10, offset=1)
                        row = ps.baseRow(self.body)

                content += row

                content += """
                        </div>
                </div>
                """

                if self.footer: content += """
                <div id="footer">
                        <div class="container">
                                %s
                        </div>
                </div>
                """ %  ps.baseRow(self.footer)

                self.page = bv.baseHTMLView()

                self.page.body = content
                self.page.title = self.title
                self.page.scripts = self.scripts
                self.page.css = self.css

                return self.page


class flagrView(smartView):
        def finishInit(self):
                flags = ps.baseIcon("flag")

#                stuffMail = ""
                stuffProfile = ""

                search = ps.baseBasicForm(
                        action=c.baseURL+"/search/flags",
                        fields=[
                                ps.baseAppend(elements=[ps.baseInput(type="text", name="search", placeholder="Search", classes="span3"), ps.baseButton("%s"%ps.baseIcon("search"), type="submit", classes="btn")])
                                ],
                        classes="form-inline navbar-form")

                if c.session.loggedIn:
                        newNote = {"name": "%s New Note Flag"%ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"}
                        newBookmark = {"name": "%s New Bookmark Flag"%ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}
#                        messCount = c.session.mail.unreadCount()
#                        readCount = c.session.mail.readCount()
#                        if messCount:
#                                messCounter = ps.baseBadge(ps.baseBadge(messCount, classes="badge-important") + " %s"%readCount, style="padding-left: 0px")
#                        else:
#                                messCounter = ps.baseBadge(str(readCount))

#                        messages = "%s %s" % (ps.baseIcon("envelope-alt"), messCounter)
                        stuffProfile = {"name": ps.baseIcon("user"), "link": c.baseURL+"/your/flags"}
                        name = "Heya %s!"%(c.session.user["username"])
                        logout = ps.baseIcon("road") + " Logout"
                        admin = ps.baseIcon("dashboard") + " Admin Panel"
                        settingLink = {"name": ps.baseIcon("cogs")+" Your settings", "link": c.baseURL+"/your/settings"}

                        adminSub = ps.baseMenu(name="adminSubDropdown",
                                        items=[{"name": ps.baseIcon("rss")+" Blog Posts", "link": c.baseURL+"/admin/posts"},
                                                {"name": ps.baseIcon("play")+" News Carousel", "link": c.baseURL+"/admin/carousels"},
                                                {"name": ps.baseIcon("group")+" Users", "link": c.baseURL+"/admin/users"}])

                        deitySub = ps.baseMenu(name="deitySubDropdown",
                                        items=[{"name": ps.baseIcon("flag")+" All the Flags", "link": c.baseURL+"/god/flags"},
                                                {"name": ps.baseIcon("search")+" Search Flags", "link": c.baseURL+"/god/search"},
                                                {"name": ps.baseIcon("magic")+" Reindex Search", "link": c.baseURL+"/god/search/reindex"}])

                        newSub = {"subName": "%s Your Profile"%ps.baseIcon("user"),
                                        "subLink": c.baseURL+"/you",
                                        "sub": ps.baseMenu(name="newSubDropdown",
                                                items=[
                                                        newNote,
                                                        newBookmark
                                                        ])
                                        }

                        if c.session.user["level"] == "GOD":
                                deity = ps.baseIcon("eye-open") + " Deity Panel"

                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[newSub,
                                                "divider",
                                                {"subName": deity, "subLink": c.baseURL+"/god", "sub": deitySub},
                                                {"subName": admin, "subLink": c.baseURL+"/admin", "sub": adminSub},
                                                "divider",
                                                settingLink,
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        elif c.session.user["level"] == "admin":
                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[newSub,
                                                "divider",
                                                {"subName": admin, "subLink": c.baseURL + "/admin", "sub": adminSub},
                                                "divider",
                                                settingLink,
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        else:
                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[newSub,
                                                "divider",
                                                settingLink,
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        link = ""
                else:
                        name = "Ohia Stranger!"
                        loginForm = ps.baseBasicForm(action=c.baseURL+"/auth/login",
                                method="POST",
                                fields=[
                                ps.baseBold("Please Login...", classes="muted"),
                                ps.baseInput(type="text", name="username", placeholder="Username"),
                                ps.baseInput(type="password", name="password", placeholder="Password"),
                                ps.baseSubmit("Login"),
                                ps.baseAButton("Register", link=c.baseURL+"/auth/register")
                                ])

                        userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[{"form": loginForm}])
                        link = ""
#                        link=ps.baseAButton("Login", link=c.baseURL+"/auth/login")

#                name = ps.baseSmall(name)

                self.navbar = ps.baseNavbar(
#                        classes="navbar-static-top",
                        classes="navbar-fixed-top",
                        brand={"name": c.appNameNav, "link": c.baseURL},
                        left=[{"form": search},
                                {"name": flags, "link": c.baseURL+"/flags"},
#                                {"name": labels, "link": c.baseURL+"/labels"}
                                ],
                        right=[stuffProfile,
#                                stuffMail,
                                link,
                                {"dropdown": userDropdown, "name": name}])

                self.footer = """
                <hr>
                %s
                """ % ps.baseSmall("A project by %s &copy 2012 %s %s" % (ps.baseAnchor(ps.baseIcon("beaker") + " transientBug", link="http://transientBug.com"), ps.baseAnchor(ps.baseIcon("github"), link="http://github.com/transientBug"), ps.baseAnchor(ps.baseIcon("twitter"), link="http://twitter.com/transientBug")))

                self.scripts += """
                <script>
                $('.btn-group').tooltip({
                      selector: "a[rel=tooltip]"
                })
                $('.nav-tabs').tooltip({
                        selector: "a[rel=tooltip]"
                })
                $('.nav-pills').tooltip({
                        selector: "a[rel=tooltip]"
                })
                </script>
                """
