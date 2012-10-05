"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseHeading.py
        A bunch of stuff to output HTML for an
        h* tag

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseHeading(b.brick):
        """
        baseHeading

        Abstract:
                Very base Heading element.

        Accepts:
                classes
                id
                content
                size

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "h"
        __tagContent__ = "content"
        __other__ = ["size"]
        def prep(self):
                self.__tag__ = "h"+str(self.size)
