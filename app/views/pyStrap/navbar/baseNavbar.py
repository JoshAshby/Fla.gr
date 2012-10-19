"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseNavbar.py
        A bunch of stuff to output HTML for a
        bootstrap navbar

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseNavbar(b.brick):
        """
        baseNavbar

        Abstract:
                Very base navbar element.

        Accepts:
                classes
                id
                brand - {"name": "", "link": ""}
                leftElements - [{"name": "", "link": "", "active": True},
                        {"search", "action"},
                        {"form": baseForm},
                        {"dropdown": baseMenu, "link": "", "name": ""},
                        {"text": ""},
                        "divider"]
                rightElements - same as left, however these are all with class .pull-right

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "div"
        __tagContent__ = "items"
        __other__ = ["left", "right", "brand"]
        def prep(self):
                self.classes.append("navbar")

                items = """<div class="navbar-inner">"""

                if self.brand:
                        items += """
                        <a href="%(link)s" class="brand">%(name)s</a>
                        """ % self.brand

                links = ""
                otherParts = ""
                linksRight = ""
                otherPartsRight = ""

                for element in self.left:
                        if type(element) is dict:
                                if element.has_key("link"):
                                        if element.has_key("active"):
                                                element["classes"] = " active "
                                        else:
                                                element["classes"] = ""

                                        links += """
                                        <li %(classes)s><a href="%(link)s">%(name)s</a></li>
                                        """ % element

                                if element.has_key("dropdown"):
                                        links += """
                                        <li class="dropdown"
                                                <a href="%(link)s" class="dropdown-toggle" data-toggle="dropdown">
                                                        %(name)s
                                                        <b class="caret"></b>
                                                </a>
                                                %(dropdown)s
                                        </li>
                                        """ % element

                                if element.has_key("text"):
                                        otherParts += """
                                        <p class="navbar-text">
                                                %(text)s
                                        </p>
                                        """ % element

                                if element.has_key("form"):
                                        otherParts += element["form"]

                        elif element == "divider":
                                links += """<li class="divider-vertical"></li>"""

                        elif element == "search":
                                otherParts += """
                                <form class="navbar-search">
                                      <input type="text" class="search-query" placeholder="Search">
                                </form>
                                """
                        else:
                                otherParts += element


                for element in self.right:
                        if type(element) is dict:
                                if element.has_key("link"):
                                        if element.has_key("active"):
                                                element["classes"] = " active "
                                        else:
                                                element["classes"] = ""

                                        linksRight += """
                                        <li %(classes)s><a href="%(link)s">%(name)s</a></li>
                                        """ % element

                                if element.has_key("dropdown"):
                                        if not element.has_key("link"): element["link"]="#"
                                        linksRight += """
                                        <li class="dropdown">
                                                <a href="%(link)s" class="dropdown-toggle" data-toggle="dropdown">
                                                        %(name)s
                                                        <b class="caret"></b>
                                                </a>
                                                %(dropdown)s
                                        </li>
                                        """ % element

                                if element.has_key("text"):
                                        otherPartsRight += """
                                        <p class="navbar-text">
                                                %(text)s
                                        </p>
                                        """ % element

                                if element.has_key("form"):
                                        otherPartsRight += element

                        elif element == "divider":
                                linksRight += """<li class="divider-vertical"></li>"""

                        elif element == "search":
                                otherPartsRight += """
                                <form class="navbar-search">
                                      <input type="text" class="search-query" placeholder="Search">
                                </form>
                                """

                        else:
                                otherPartsRight += element


                items += """
                                <ul class="nav pull-left">
                                        %(links)s
                                </ul>
                                <div class="pull-left">
                                        %(otherParts)s
                                </div>
                                <div class="pull-right">
                                        %(otherPartsRight)s
                                </div>
                                <ul class="nav pull-right">
                                        %(linksRight)s
                                </ul>
                        </div>
                """ % {"links": links, "otherParts": otherParts, "otherPartsRight": otherPartsRight, "linksRight": linksRight}

                self.items = items
