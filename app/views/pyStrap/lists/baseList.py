"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseList.py
        A bunch of stuff to output HTML for a
        base list - ul/ol list.

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseUL(b.brick):
        """
        baseUL

        Abstract:
                Very base ul element.
        Accepts:
                kwarg elements - [] a list of li elements to include in the list.

        Returns:
                str - an HTML ul element

        """
        __tag__ = "ul"
        __tagContent__ = "items"
        def prep(self):
                content = ""
                for element in self.items:
                        content += element

                self.items = content


class baseOL(b.brick):
        """
        baseOL

        Abstract:
                Very base ol element.
        Accepts:
                kwarg elements - [] a list of li elements to include in the list.

        Returns:
                str - an HTML ol element

        """
        __tag__ = "ol"
        __tagContent__ = "items"
        def prep(self):
                content = ""
                for element in self.items:
                        content += element

                self.items = content
