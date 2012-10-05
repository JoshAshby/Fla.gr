"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseThumbnail.py
        A bunch of stuff to output HTML for a
        bootstrap thumbnail grids.

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseImageThumbnail(b.brick):
        """
        baseImageThumbnail

        Abstract:
                Very base thumbnail element.
        Accepts:
                classes
                id
                link
                source
                alt

        Returns:
                str - an HTML li element

        """
        __tag__ = "li"
        __tagContent__ = "content"
        __other__ = ["alt", "source", "link", "width"]
        __tagContent__ = "content"
        def prep(self):
                if self.width: self.classes.append(" span%s " % str(self.width))
                self.content = """<a href="%(link)s" class="thumbnail">
        <img src="%(source)s" alt="%(alt)s">
</a>""" % self


class baseTextThumbnail(b.brick):
        """
        baseTextThumbnail

        Abstract:
                Very base thumbnail element.
        Accepts:
                classes
                id
                label
                caption

        Returns:
                str - an HTML li element

        """
        __tag__ = "li"
        __other__ = ["caption", "label", "width"]
        __tagContent__ = "content"
        def prep(self):
                if self.width: self.classes.append(" span%s " % str(self.width))
                self.content = """<div class="thumbnail">
        <h3>%(label)s</h3>
        <p>%(caption)s</p>
</div>
                """ % self

class baseImageTextThumbnail(b.brick):
        """
        baseImageTextThumbnail

        Abstract:
                Very base thumbnail element.
        Accepts:
                classes
                id
                source
                alt
                label
                caption

        Returns:
                str - an HTML li element

        """
        __tag__ = "li"
        __other__ = ["caption", "label", "source", "alt", "width"]
        __tagContent__ = "content"
        def prep(self):
                if self.width: self.classes.append(" span%s " % str(self.width))
                self.content = """<div class="thumbnail">
        <img src="%(source)s" alt="%(alt)s">
        <h3>%(label)s</h3>
        <p>%(caption)s</p>
</div>
                """ % self
