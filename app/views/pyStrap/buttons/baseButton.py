"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseButton.py
        A bunch of stuff to output HTML for a
        bootstrap button.

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseAButton(b.brick):
        """
        baseAButton

        Abstract:
                Very base button with the anchor element.

        Accepts:
                classes
                id
                content
                link
                disable

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "a"
        __tagContent__ = "content"
        __other__ = ["disable"]
        __tagAttr__ = ["link", "rel", "title"]
        def prep(self):
                self.classes.append("btn")
                if self.disable: self.classes.append("disabled")


class baseButton(b.brick):
        """
        baseButton

        Abstract:
                Very base button with the button element.

        Accepts:
                classes
                id
                content
                disable

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "button"
        __tagContent__ = "content"
        def prep(self):
                self.classes.append("btn")


class baseSubmit(b.brick):
        """
        baseSubmit

        Abstract:
                Very base submit button with the button element.

        Accepts:
                classes
                id
                content
                disable

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "button"
        __tagAttr__ = ["type"]
        __tagContent__ = "content"
        def prep(self):
                self.classes.append("btn")
                self.classes.append("btn-primary")
                self.type = "submit"
