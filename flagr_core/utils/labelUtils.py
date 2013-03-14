#!/usr/bin/env python
"""
utils for handling getting all the labels from a list of flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
def listLabels(flags, showAll):
    labels = []
    for flag in flags:
        if showAll:
            labels.extend(flag.labels)
        else:
            if flag.visibility:
                labels.extend(flag.labels)
    return labels
