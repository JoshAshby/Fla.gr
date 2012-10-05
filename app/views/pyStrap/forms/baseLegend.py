"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseLegend.py
        A bunch of stuff to output HTML for an
        legend tag

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseLegend(b.brick):
        """
        baseLegend

        Abstract:
                Very base Legend element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "legend"
        __tagContent__ = "content"
