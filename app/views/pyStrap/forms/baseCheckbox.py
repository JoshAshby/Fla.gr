"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseCheckbox.py
        A bunch of stuff to output HTML for a
        checkbox

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b
import views.pyStrap.forms.baseInput as bi


class baseCheckbox(b.brick):
        """
        baseCheckbox

        Abstract:
                Very base checkboxe element.

        Accepts:
                classes
                id
                label
                value
                name
                checked

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "label"
        __tagContent__ = "content"
        __other__ = ["checked", "value", "name", "label"]
        def prep(self):
                self.classes.append("checkbox")

                self.content = bi.baseInput(type="checkbox", value=self.value, name=self.name, id=self.id, checked=self.checked) + self.label
