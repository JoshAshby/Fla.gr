"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseItalic.py
        A bunch of stuff to output HTML for an
        em tag

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseItalic(b.brick):
        """
        baseItalic

        Abstract:
                Very base Italics element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "em"
        __tagContent__ = "content"
