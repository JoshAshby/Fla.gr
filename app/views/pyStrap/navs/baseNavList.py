"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseNavList.py
        A bunch of stuff to output HTML for a
        base bootstrap nav list

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseNavList(b.brick):
        """
        baseNavList

        Abstract:
                Very base nav list element

        Accepts:
                elements - [{"name": "", "link": "", "active": Boolean},
                "divider",
                {"header": ""}]

        Returns:
                str - an HTML ul element

        """
        __tag__ = "ul"
        __tagContent__ = "items"
        def prep(self):
                self.classes.extend(["nav", "nav-list"])

                content = ""
                for element in self.items:
                       if element == "divider":
                                content += """<li class="divider"></li>"""

                       else:
                                if not element.has_key("classes"): element["classes"] = ""

                                if element.has_key("name"):
                                        if element.has_key("active"):
                                                element["classes"] += " active "
                                        content += """
                                        <li class="%(classes)s"><a href="%(link)s">%(name)s</a></li>
                                        """ % element

                                if element.has_key("header"):
                                        content += """
                                        <li class="nav-header">%(header)s</li>
                                        """ % element

                                if element.has_key("text"):
                                        content += """
                                        <li classes="">%(text)s</li>
                                        """ % element


                self.items = content
