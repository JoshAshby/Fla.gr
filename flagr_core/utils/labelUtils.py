#!/usr/bin/env python
"""
utils for handling getting all the labels from a list of flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
def listLabels(flags):
    labels = []
    for flag in flags:
        labels.extend(flag.labels)
    return labels
