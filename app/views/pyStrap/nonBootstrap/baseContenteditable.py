"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseContenteditable.py
        

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseContenteditable(b.brick):
        """
        baseContenteditable

        Abstract:
                Very base div element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tagContent__ = "content"
        __tagAttr__ = ["contenteditable"]
        __tag__ = "div"
        __other__ = ["tag"]
        def prep(self):
                self.__tag__ = self.tag
                self.contenteditable = "true"


class baseEditableScript(b.brick):
        """
        baseEditableScript

        Abstract:
                Very base script element.

        Accepts:
                classes
                id
                content

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tagContent__ = "content"
        __tag__ = "script"
        __other__ = ["formID", "elementID"]
        def prep(self):
                if type(self.formID) == str and type(self.elementID) == str:
                        self.content = """function getContent(){document.getElementById("%s").value = document.getElementById("%s").innerHTML;}""" % (self.formID, self.id)

                else:
                        self.content = "function getContent(){"
                        for part in range(len(self.formID)):
                                self.content += """
document.getElementById("%s").value = document.getElementById("%s").innerHTML;
""" % (self.formID[part], self.elementID[part])

                        self.content += """ } """
