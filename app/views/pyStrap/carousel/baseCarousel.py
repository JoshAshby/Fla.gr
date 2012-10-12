"""
pyStrap V1
A HTML gui generation system with the intent of
being used with Twitter's Bootstrap 2.2.1. The
Aim is to create a something that functions a
little like QT or wxWidgets for making GUI's
However just with the web as the target platform

baseCarousel.py
        A bunch of stuff to output HTML for a
        bootstrap carousel

JoshAshby 2012
http://JoshAshby.com
http://github.com/JoshAshby
"""
import views.pyStrap.brick as b


class baseCarousel(b.brick):
        """
        baseCarousel

        Abstract:
                Very base carousel element using the div 

        Accepts:
                classes
                id
                name
                elements - []

        Returns:
                str - String of HTML once every one of its elements
                have been built.

        """
        __tag__ = "div"
        __tagContent__ = "content"
        __other__ = ["items"]
        def prep(self):
                self.classes.append("carousel slide")

                links = """
                <!-- Carousel items -->
                        <div class="carousel-inner">
                """
                links += """<div class="item active">%s</div>""" % self.items[0]

                for element in self.items[1:]:
                        links += """<div class="item">%s</div>""" % element


                links += """
                        </div>
                        <!-- Carousel nav -->
                        <a class="carousel-control left" href="#%(id)s" data-slide="prev">&lsaquo;</a>
                        <a class="carousel-control right" href="#%(id)s" data-slide="next">&rsaquo;</a>""" % self

                self.content = links
