"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseWell.py
        A bunch of stuff to output HTML for an
        div tag with well class

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import flagr.views.pyStrap.brick as b


class baseWell(b.brick):
        """
        baseWell

        Abstract:
                Very base Well element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "div"
        __tagContent__ = "content"
        def prep(self):
                self.classes.append("well")