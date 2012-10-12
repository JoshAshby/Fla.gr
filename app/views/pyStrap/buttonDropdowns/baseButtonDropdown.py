"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseButtonDropdown.py
        A bunch of stuff to output HTML for a
        base button dropdown

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b
import views.pyStrap.buttons.baseButton as btn

class baseButtonDropdown(b.brick):
        """
        baseButtonDropdown

        Abstract:
                Very base button dropdown element.

        Accepts:
                content - baseMenu
                name
                classes
                id

        Returns:
                str - an HTML div element

        """
        __other__ = ["btn", "dropdown"]
        __tag__ = "div"
        __tagContent__ = "content"
        def prep(self):
                classes = ""
                for each in self.classes:
                        classes += " %s " % each

                self.btn["classes"].union({"dropdown-toggle"})
                self.btn["data"].append(("toggle", "dropdown"))

                self.content = self.btn + self.dropdown


class baseSplitDropdown(b.brick):
        """
        baseSplitADropdown

        Abstract:
                Very base button dropdown element.

        Accepts:
                content - baseMenu
                name
                classes
                id

        Returns:
                str - an HTML div element

        """
        __tag__ = "div"
        __tagContent__ = "content"
        __other__ = ["btn", "dropdown", "dropBtn"]
        def prep(self):
                self.content = self.btn + self.dropBtn + self.dropdown
                self.classes.append("btn-group")
