"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

brick.py
        Aims at making a common interface for all
        or most units.

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""

class brick(object):
        """
        brick

        Abstract:


        Accepts:
                Anything! YAY. On the other hand, please make sure
                everything uses a fairly common interface.
                        * content/elements/fields

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __defaultParts__ = ["classes", "id", "style", "rel"]
        __tag__ = ""
        __tagAttr__ = []
        __tagContent__ = ""
        __other__ = []
        def __init__(self, *args, **kwargs):
                """

                """

                self.data = []
                self.checked = False

                for part in self.__defaultParts__:
                        setattr(self, part, "")

                for part in self.__tagAttr__:
                        setattr(self, part, "")

                setattr(self, self.__tagContent__, "")

                for part in self.__other__:
                        setattr(self, part, "")

                self.classes = []

                for kwarg in kwargs:
                        if kwarg == "classes":
                                self.classes.append(kwargs[kwarg])
                        else:
                                setattr(self, kwarg, kwargs[kwarg])

                self.args = args

                self.returnHTML = ""

        def __repr__(self):
                self.build()
                return str(self.returnHTML)

        def __str__(self):
                self.build()
                return str(self.returnHTML)

        def __unicode__(self):
                self.build()
                return u"%s" % str(self.returnHTML)

        def __add__(self, other):
                self.build()
                return str(self.returnHTML)+other

        def __radd__(self, other):
                self.build()
                return other+str(self.returnHTML)

        def __getattr__(self, item):
                return object.__getattribute__(self, item)

        def __getitem__(self, item):
                return object.__getattribute__(self, item)

        def __setattr__(self, item, value):
                return object.__setattr__(self, item, value)

        def __setitem__(self, item, value):
                return object.__setattr__(self, item, value)

        def prep(self):
                """
                This gets over ridden by all objects that subclass brick
                        The purpose of build is to generate the HTML
                        that the object is designed for, so that later
                        it can be used much like a string variable
                        to be thrown into the final template.
                """
                pass

        def build(self):
                if self.args:
                        setattr(self, self.__tagContent__, self.args[0])

                self.prep()

                self.returnHTML = "<%s " % self.__tag__
                for part in self.__defaultParts__:
                        if part == "classes":
                                classes = ""
                                for bit in self.classes:
                                        classes += " %s " % bit
                                self.returnHTML += """ class="%s" """ % classes

                        elif getattr(self, part):
                                self.returnHTML += """ %s="%s" """ % (part, getattr(self, part))

                for part in self.__tagAttr__:
                        if part == "link":
                                self.returnHTML += """ href="%s" """ % self.link
                        else:
                                if getattr(self, part):
                                        self.returnHTML += """ %s="%s" """ % (part, getattr(self, part))

                for part in self.data:
                        self.returnHTML += """ data-%s="%s" """ % (part[0], part[1])


                if self.__tag__ == "input":
                        if self.checked:
                                checked = "checked"
                        else:
                                checked = ""
                        self.returnHTML += "%s>"%checked

                elif self.__tag__ == "i":
                        self.returnHTML += "></%s>" % self.__tag__

                else:
                        self.returnHTML += ">%s</%s>" % (getattr(self, self.__tagContent__), self.__tag__)

