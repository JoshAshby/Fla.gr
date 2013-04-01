#!/usr/bin/env python
"""
utils for handling getting all the labels from a list of flags
"""


def listLabels(flags, showAll):
    """
    Generates a list of labels from all given flags.

    :param flags: List of dicts which represent flags
    :type flags: List
    :param showAll: True or False to show all flags or only public flag labels
    :type showAll: Boolean
    :return: List of labels
    :rtype: List of Str
    """
    labels = []
    for flag in flags:
        if showAll:
            labels.extend(flag.labels)
        else:
            if flag.visibility:
                labels.extend(flag.labels)
    return labels
