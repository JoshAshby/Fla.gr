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
        __other__ = ["name"]
        __tag__ = "div"
        __tagContent__ = "content"
        def prep(self):
                classes = ""
                for each in self.classes:
                        classes += " %s " % each
                self.content = """<a class="btn dropdown-toggle %s" data-toggle="dropdown" href="#">
        %s
        <span class="caret"></span>
</a>
%s""" % (classes, self.name, self.content)


class baseSplitADropdown(b.brick):
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
        __other__ = ["link", "name", "btnClasses"]
        def prep(self):
                self.link = self.link or "#"
                self.classes.append("btn-group")
                self.content = """<a class="btn %s" href="%s">
        %s
</a>
<button class=" btn dropdown-toogle %s" data-toggle="dropdown">
        <span class="caret"></span>
</button>
%s""" % (self.btnClasses, self.link, self.name, self.btnClasses, self.content)


class baseSplitButtonDropdown(b.brick):
        """
        baseSplitButtonDropdown

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
        __other__ = ["name", "btnClasses"]
        def prep(self):
                self.link = self.link or "#"
                self.classes.append("btn-group")

                self.content = """<button class="btn %s"">
        %s
</button>
<button class=" btn dropdown-toogle %s" data-toggle="dropdown">
        <span class="caret"></span>
</button>
%s""" % (self.btnClasses, self.name, self.btnClasses, self.content)
