"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseColumn.py
        A bunch of stuff to output HTML for a
        bootstrap column.

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseColumn(b.brick):
        """
        baseLabel

        Abstract:
                Very base column element.
        Accepts:
                width
                offset
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "div"
        __other__ = ["width", "offset"]
        __tagContent__ = "content"
        def prep(self):
                self.classes.append((" span%s " % str(self.width)) or "")
                self.classes.append((" offset%s " % str(self.offset)) or "")
