"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseFormHelp.py
        A bunch of stuff to output HTML for an
        span tag with class help-block

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseFormHelp(b.brick):
        """
        baseFormHelp

        Abstract:
                Very base FormHelp element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __parts__= ["classes", "id", "content"]
        def build(self):
                self.returnHTML = """
                <span class="help-block %(classes)s" id="%(id)s">
                        %(content)s
                </span>
                """ % self.parts

                return self.returnHTML
