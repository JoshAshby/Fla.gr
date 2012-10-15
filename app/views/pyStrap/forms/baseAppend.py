"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseAppend.py
        A bunch of stuff to output HTML for a
        bootstrap append

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b
import views.pyStrap.forms.baseInput as bi


class baseAppend(b.brick):
        """
        baseAppend

        Abstract:
                Very base append element.

        Accepts:
                elements

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "div"
        __tagContent__ = "content"
        __other__ = ["elements"]
        def prep(self):
                self.classes.append("input-append")

                self.content = ""

                for element in self.elements:
                        self.content += element
