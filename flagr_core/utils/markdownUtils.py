#!/usr/bin/env python
"""
utils for handling unsafe markdown
renders and cleans

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import bleach as bl
import markdown as md

cleanTags = bl.ALLOWED_TAGS
cleanTags.append(['p', 'img', 'small', 'pre'])
cleanAttr = bl.ALLOWED_ATTRIBUTES
cleanAttr["img"] = ["src", "width", "height"]
cleanAttr["i"] = ["class"]

def markClean(markdown):
    mark = md.markdown(markdown)
    cleanedMark = bl.clean(mark, cleanTags, cleanAttr)

    return cleanedMark
