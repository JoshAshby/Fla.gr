#!/usr/bin/env python2
"""


For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import models.carousels.newsCarousel as nc
import models.blocks.helpers as helpers
import markdown

def carousel(id=None, md=False):
        if id:
                key = id.strip("newsCarousel:")
                returnCar = nc.newsCarousel(key)
                if md:
                        returnCar["content"] = markdown.markdown(returnCar["content"])
        if not id:
                returnCar = nc.newsCarousel()

        return returnCar

def carouselList(md=False):
        keys = c.redisCarouselServer.keys("newsCarousel:*:id")
        carouselList = []
        def addCarousel(key):
                returnCarousel = carousel(key)
                if md:
                        returnCarousel["content"] = markdown.markdown(returnCarousel["content"])

                carouselList.append(returnCarousel)

        for key in keys:
                key = key.strip(":id")
                addCarousel(key)

        return carouselList
