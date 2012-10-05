"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseIcon.py
        A bunch of stuff to output HTML for a
        bootstrap icon

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseIcon(b.brick):
        """
        baseIcon

        Abstract:
                Very base icon element.
        Accepts:
                icon

        Returns:
                str - an HTML i element

        """
        __tag__ = "i"
        __tagContent__ = "icon"
        def prep(self):
                if type(self.icon) == str:
                        self.classes.append("icon-%s" % self.icon)
                else:
                        for icon in self.icon:
                                self.classes.append("icon-%s" % icon)
