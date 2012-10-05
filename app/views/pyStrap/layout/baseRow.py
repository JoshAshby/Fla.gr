"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseRow.py
        A bunch of stuff to output HTML for a
        bootstrap row.

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseRow(b.brick):
        """
        baseRow

        Abstract:
                Very base row element.
        Accepts:
                fluid
                columns

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "div"
        __other__ = ["fluid", "columns"]
        __tagContent__ = "content"
        def prep(self):
                if self.fluid: fluid = "-fluid"
                else: fluid = ""
                self.classes.append("row%s" % fluid)
                columns = self.content

                content = ""

                if type(columns) is list:
                        for column in columns:
                                content += column
                else:
                        content = columns

                self.content = content
