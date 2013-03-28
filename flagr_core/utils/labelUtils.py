#!/usr/bin/env python
"""
utils for handling getting all the labels from a list of flags
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
