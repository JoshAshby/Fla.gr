"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseSmall.py
        A bunch of stuff to output HTML for an
        small tag

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import flagr.views.pyStrap.brick as b


class baseSmall(b.brick):
        """
        baseSmall

        Abstract:
                Very base Small element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "small"
        __tagContent__ = "content"