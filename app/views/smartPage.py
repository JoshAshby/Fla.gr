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
        __defaultParts__ = [ "title", "navbar", "header", "sidebar", "body", "footer", "page", "messages", "fluid"]
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
                        self.body = ps.baseColumn(self.body, width=8, offset=2)
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


class flagrPage(smartPage):
        def finishInit(self):
                home = ps.baseIcon(icon="home")+" Home"
                flags = ps.baseIcon(icon="flag")+" Flags"

                if c.session.loggedIn == "True":
                        name = "Heya %s!"%(c.session.user.username)
                        logout = ps.baseIcon("road") + " Logout"
                        admin = ps.baseIcon("dashboard") + " Admin Panel"
                        flagLink = {"name": ps.baseIcon("flag")+" Your flags", "link": "/flags"}
                        profileLink = {"name": ps.baseIcon("user")+" Your profile", "link": "/profiles"}

                        if c.session.user.level == "GOD":
                                deity = ps.baseIcon("eye-open") + " Deity Panel"

                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[flagLink,
                                                profileLink,
                                                "divider",
                                                {"name": deity, "link": c.baseURL+"/god"},
                                                {"name": admin, "link": c.baseURL+"/admin"},
                                                "divider",
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        elif c.session.user.level == "admin":
                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[flagLink,
                                                profileLink,
                                                "divider",
                                                {"name": "Admin Panel", "link": c.baseURL + "/admin"},
                                                "divider",
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])

                        else:
                                userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[flagLink,
                                                profileLink,
                                                "divider",
                                                {"name": logout, "link": c.baseURL+"/auth/logout"}])
                else:
                        name = "Ohia Stranger!"
                        loginForm = ps.baseBasicForm(action=c.baseURL+"/auth/login",
                                method="POST",
                                fields=[
                                ps.baseInput(type="text", name="username", placeholder="Username"),
                                ps.baseInput(type="password", name="password", placeholder="Password"),
                                ps.baseSubmit(content="Login")
                                ])
                        userDropdown = ps.baseMenu(name="userDropdown",
                                        items=[{"header": "Please login to continue..."},
                                                {"form": loginForm}])


                self.navbar = ps.baseNavbar(
                        classes="navbar-static-top",
                        brand={"name": c.appName, "link": c.baseURL},
                        left=[{"name": ps.baseIcon("home")+" Home", "link": c.baseURL},
                                "divider",
                                {"name": flags, "link": c.baseURL + "/flags"}],
                        right=[{"dropdown": userDropdown, "name": name}])

                self.footer = """
                <hr>
                %s
                """ % ps.baseParagraph("A project by %s &copy 2012 | %s | %s" % (ps.baseAnchor(ps.baseIcon("user") + " JoshAshby", link="http://joshashby.com"), ps.baseAnchor(ps.baseIcon("github"), link="http://github.com/JoshAshby"), ps.baseAnchor(ps.baseIcon("twitter"), link="http://twitter.com/JoshPAshby")))

