"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseForm.py
        A bunch of stuff to output HTML for a
        base bootstrap horizontal form

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseHorizontalForm(b.brick):
        """
        baseHorizontalForm

        Abstract:
                Very base form element.

        Accepts:
                elements - [{"label": "", "content": base, "help": "", "classes": ""}]
                actionElements - [base]
                action
                method

        Returns:
                str - an HTML form element

        """
        __tag__ = "form"
        __tagAttr__ = ["action", "method", "onsubmit"]
        __tagContent__ = "fields"
        __other__ = ["actions"]
        def prep(self):
                returnHTML = ""
                self.classes.append("form-horizontal")
                for element in self.fields:
                        if type(element) == dict:
                                if element.has_key("help"):
                                        element["help"] = """
                                                <span class="help-block">%s</span>
                                        """ % element["help"]
                                else:
                                        element["help"] = ""

                                if not element.has_key("classes"): element["classes"] = ""

                                if element.has_key("label"):
                                        returnHTML += """
                                        <div class="control-group %(classes)s">
                                                <label class="control-label">%(label)s</label>
                                                <div class="controls">
                                                        %(content)s
                                                        %(help)s
                                                </div>
                                        </div>
                                        """ % element

                                else:
                                        returnHTML += """
                                        %(content)s
                                        %(help)s
                                        """ % element
                        else:
                                returnHTML += element

                returnHTML += """
                        <div class="form-actions">
                """

                for element in self.actions:
                        returnHTML += element

                returnHTML += """
                        </div>
                """
                self.fields = returnHTML


class baseBasicForm(b.brick):
        """
        baseBasicForm

        Abstract:
                Very base form element.

        Accepts:
                elements - []
                action
                method

        Returns:
                str - an HTML form element

        """
        __tag__ = "form"
        __tagContent__ = "fields"
        __tagAttr__ = ["action", "method"]
        def prep(self):
                content = ""

                for element in self.fields:
                        content += element

                self.fields = content
