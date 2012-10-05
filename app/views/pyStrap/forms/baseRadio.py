"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseRadio.py
        A bunch of stuff to output HTML for a
        radio

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b
import views.pyStrap.forms.baseInput as baseInput



class baseRadio(b.brick):
        """
        baseRadio

        Abstract:
                Very base radio element.

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
                self.classes.append("radio")

                if self.checked: self.checked = "checked"

                self.content = baseInput(type="radio", value=self.vale, name=self.name, id=self.id) + self.label
