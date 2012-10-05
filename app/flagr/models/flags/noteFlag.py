#!/usr/bin/env python2
"""
Fla.gr - Personal Memory
Model for working with note type flags


For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import flagr.models.baseFlag as bf
import models.blocks.helpers as helpers


class noteFlag(bf.baseFlag):
        fields = ["title",
                "description",
                ("labels", "set"),
                "time",
                ("visibility", "string", helpers.boolean),
                "author",
                "userID",
                "flagType"]
        flag = "note"
        icon = "list-alt"
