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
import views.pyStrap.pyStrap as ps
import views.basePage as bp


class smartPage(object):
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
        __defaultParts__ = [ "title", "navbar", "header", "sidebar", "body", "footer", "page", "messages", "fluid", "scripts"]
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

                if c.session.messages:
                        self.messages = ps.baseRow(ps.baseColumn(c.session.messages, width=10, offset=1))

                content += self.messages

                if self.sidebar:
                        self.sidebar = ps.baseColumn(self.sidebar, width=4)
                        self.body = ps.baseColumn(self.body, width=8)

                        row = ps.baseRow([self.sidebar, self.body])

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

                self.page = bp.basePage()

                self.page.build()

                self.page.content = content
                self.page.title = self.title
                self.page.scripts = self.scripts


class flagrPage(smartPage):
        def finishInit(self):
                home = ps.baseIcon(icon="home")
                flags = ps.baseIcon(icon="flag")+" Flags"
                public = ps.baseIcon("flag") + " Public Flags"
                labels = ps.baseIcon("tags") + " Public Labels"

                stuffFlag = ""
                stuffLabel = ""
                stuffUser = ""
                stuffMail = ""
                div = ""

                if c.session.loggedIn:
                        messCount = c.session.mail.unreadCount()
                        readCount = c.session.mail.readCount()
                        if messCount:
                                messCounter = ps.baseBadge(ps.baseBadge(messCount, classes="badge-important") + " %s"%readCount, style="padding-left: 0px")
                        else:
                                messCounter = ps.baseBadge(str(readCount))

                        messages = "%s %s" % (ps.baseIcon("envelope-alt"), messCounter)
                        stuffMail = {"name": messages, "link": "/your/messages"}
                        stuffFlag = {"name": ps.baseIcon("flag"), "link": "/your/flags"}
                        stuffLabel = {"name": ps.baseIcon("tags"), "link": "/your/labels"}
                        stuffUser = {"name": ps.baseIcon("user"), "link": "/you"}
                        div = "divider"
                        name = "Heya %s!"%(c.session.user["username"])
                        logout = ps.baseIcon("road") + " Logout"
                        admin = ps.baseIcon("dashboard") + " Admin Panel"
                        flagLink = {"name": ps.baseIcon("flag")+" Your flags", "link": "/your/flags"}
                        labelLink = {"name": ps.baseIcon("tags") +" Your labels", "link": "/your/labels"}
                        profileLink = {"name": ps.baseIcon("user")+" You", "link": "/you"}

                        adminSub = ps.baseMenu(name="adminSubDropdown",
                                        items=[{"name": ps.baseIcon("rss")+" Blog Posts", "link": c.baseURL+"/admin/posts"},
                                                {"name": ps.baseIcon("play")+" News Carousel", "link": c.baseURL+"/admin/carousels"},
                                                {"name": ps.baseIcon("group")+" Users", "link": c.baseURL+"/admin/users"}])

                        deitySub = ps.baseMenu(name="deitySubDropdown",
                                        items=[{"name": ps.baseIcon("flag")+" All flags", "link": c.baseURL+"/god/flags"},
                                                {"name": ps.baseIcon("tags")+" All labels", "link": c.baseURL+"/god/labels"}])

                        youSub = {"subName": "%s You"%ps.baseIcon("user"),
                                "subLink": c.baseURL+"/you",
                                "sub": ps.baseMenu(name="youSubDropdown",
                                        items=[
                                                flagLink,
                                                labelLink
                                                ]
                                        )
                                }

                        if c.session.user["level"] == "GOD":
                                deity = ps.baseIcon("eye-open") + " Deity Panel"

                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[profileLink,
                                                "divider",
                                                {"subName": deity, "subLink": c.baseURL+"/god", "sub": deitySub},
                                                {"subName": admin, "subLink": c.baseURL+"/admin", "sub": adminSub},
                                                "divider",
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        elif c.session.user["level"] == "admin":
                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[profileLink,
                                                "divider",
                                                {"subName": admin, "subLink": c.baseURL + "/admin", "sub": adminSub},
                                                "divider",
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        else:
                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[profileLink,
                                                "divider",
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])
                        link=""
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
                        link={"name": "Login", "link": c.baseURL+"/auth/login"}
                        link=ps.baseAButton("Login", link=c.baseURL+"/auth/login")


                self.navbar = ps.baseNavbar(
                        classes="navbar-static-top",
                        brand={"name": c.appName, "link": c.baseURL},
                        left=[{"name": home, "link": c.baseURL},
                                "divider",
                                {"name": public, "link": c.baseURL + "/flags"},
                                {"name": labels, "link": c.baseURL+"/labels"}],
                        right=[stuffFlag,
                                stuffLabel,
                                stuffMail,
                                div,
                                link,
                                {"dropdown": userDropdown, "name": name}])

                self.footer = """
                <hr>
                %s
                """ % ps.baseParagraph("A %s production &copy 2012 %s %s" % (ps.baseAnchor(ps.baseIcon("beaker") + " transientBug", link="http://joshashby.com"), ps.baseAnchor(ps.baseIcon("github"), link="http://github.com/JoshAshby"), ps.baseAnchor(ps.baseIcon("twitter"), link="http://twitter.com/JoshPAshby")))

