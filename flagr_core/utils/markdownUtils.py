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
    """
    Renders the given markdown, then leans and escapes most HTML
    tags

    :param markdown: String of makrdown
    :type markdown: Str
    :return: Rendered Markdown with escaped HTML
    :rtype: Str
    """
    mark = md.markdown(markdown)
    cleanedMark = bl.clean(mark, tags=cleanTags, attributes=cleanAttr)

    return cleanedMark

def mark(markdown):
    """
    Renders the given markdown

    :param markdown: A markdown document
    :type markdown: Str
    :return: Rendered markdown
    :rtype: Str
    """
    return md.markdown(markdown)


def cleanInput(preClean):
    """
    Escapes HTML

    :param preClean: Input such as from a form which may contain HTML that
        needs to be escaped
    :type preClean: Str
    :return: Escaped HTML input
    :rtype: Str
    """
    return bl.clean(preClean, tags=cleanTags, attributes=cleanAttr)
