"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseButtonGroup.py
        A bunch of stuff to output HTML for a
        base button group

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseButtonGroup(b.brick):
        """
        baseButtonGroup

        Abstract:
                Very base button group element.

        Accepts:
                elements - [] a list of button elements to include in the group

        Returns:
                str - an HTML div element

        """
        __tag__ = "div"
        __tagContent__ = "buttons"
        def prep(self):
                self.classes.append("btn-group")

                buttons = self.buttons
                self.buttons = ""

                for button in buttons:
                        self.buttons += button


class baseButtonToolbar(b.brick):
        """
        baseButtonToolbar

        Abstract:
                Very base button toolbar element.

        Accepts:
                elements - [] a list of button group elements to include in the
                        toolbar group

        Returns:
                str - an HTML div element

        """
        __tag__ = "div"
        __tagContent__ = "buttonGroups"
        def prep(self):
                self.classes.append("btn-toolbar")

                buttons = self.buttonGroups
                self.buttonGroups = ""

                for button in buttons:
                        self.buttonGroups += button

