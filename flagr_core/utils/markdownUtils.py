#!/usr/bin/env python
"""
utils for handling unsafe markdown
renders and cleans
"""
import bleach as bl
import markdown as md

cleanTags = bl.ALLOWED_TAGS
cleanTags.extend(['p', 'img', 'small', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','br'])
cleanAttr = bl.ALLOWED_ATTRIBUTES
cleanAttr["img"] = ["src", "width", "height"]
cleanAttr["i"] = ["class"]

def markClean(markdown):
    mark = md.markdown(markdown)
    cleanedMark = bl.clean(mark, tags=cleanTags, attributes=cleanAttr)

    return cleanedMark

def mark(markdown):
    return md.markdown(markdown)


def cleanInput(preClean):
    return bl.clean(preClean, tags=cleanTags, attributes=cleanAttr)
