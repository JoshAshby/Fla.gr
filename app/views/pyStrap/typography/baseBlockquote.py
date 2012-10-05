"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseBlockquote.py
        A bunch of stuff to output HTML for an
        blockquote tag

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseBlockquote(b.brick):
        """
        baseBlockquote

        Abstract:
                Very base Blockquote element.

        Accepts:
                classes
                id
                content
                source

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "blockquote"
        __tagContent__ = "content"
