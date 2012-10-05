"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseInput.py
        A bunch of stuff to output HTML for a
        input

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseInput(b.brick):
        """
        baseInput

        Abstract:
                Very base input element.

        Accepts:
                classes
                id
                name
                placeholder
                type

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "input"
        __tagAttr__ = ["name", "type", "placeholder", "value"]
        __tagContent__ = "content"
