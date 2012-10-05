"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseTextarea.py
        A bunch of stuff to output HTML for a
        Textarea

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseTextarea(b.brick):
        """
        baseTextarea

        Abstract:
                Very base Textareae element.

        Accepts:
                classes
                id
                value
                name
                rows

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "textarea"
        __tagAttr__ = ["name", "rows"]
        __tagContent__ = "content"
        def prep(self):
                if not self.rows: self.rows=10
