"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseMenu.py
        A bunch of stuff to output HTML for a
        bootstrap dropdown menu

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseMenu(b.brick):
        """
        baseMenu

        Abstract:
                Very base dropdown element using the div 

        Accepts:
                classes
                id
                name
                elements - [{"name": "", "link": ""},
                {"sub": baseMenu, "link": "", "name": ""},
                "divider",
                {"header": ""},
                {"text": ""},
                {"form": baseForm}]

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "ul"
        __tagContent__ = "items"
        __tagAttr__ = ["role"]
        def prep(self):
                self.classes.append("dropdown-menu")

                links = ""

                for element in self.items:
                        if element == "divider":
                                links += """<li class="divider"></li>"""

                        else:
                                if element.has_key("link"):
                                        links += """
                                        <li><a tabindex="-1" href="%(link)s">%(name)s</a></li>
                                        """ % element

                                if element.has_key("sub"):
                                        links += """
                                        <li class="dropdown-submenu">
                                                <a tabindex="-1" href="%(subLink)s">%(subName)s</a>
                                                %(sub)s
                                        </li>
                                        """ % element

                                if element.has_key("form"):
                                        links += """
                                        <li style="padding: 20px">%s</li>
                                        """ % element["form"]

                                if element.has_key("header"):
                                        links += """
                                        <li><strong>%s</strong></li>
                                        """ % element["header"]

                                if element.has_key("text"):
                                        links += """
                                        <li>%s</li>
                                        """ % element["text"]

                self.items = links
