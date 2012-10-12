"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseSelect.py
        A bunch of stuff to output HTML for a
        base select input

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseSelect(b.brick):
        """
        baseSelect

        Abstract:
                Very base select element.
        Accepts:
                kwarg elements - [] a list of li elements to include in the list.

        Returns:
                str - an HTML ul element

        """
        __tag__ = "select"
        __tagContent__ = "items"
        __other__ = ["elements"]
        __tagAttr__ = ["name"]
        def prep(self):
                content = ""
                for element in self.elements:
                        if element.has_key("selected"):
                                element["selected"] = """selected="selected" """
                        else:
                                element["selected"] = ""
                        content += """<option value="%(value)s" %(selected)s>%(label)s</option>"""%element

                self.items = content
