#!/usr/bin/env python
"""
utils for making a pagination unit

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""

class pagination(object):
    """
    Wrapper for pagination units in templates.
    """
    def __init__(self, items, perPage, currentPage):
        self._items = items
        self.perPage = perPage
        self.currentPage = currentPage
        self._len = len(items)

    @property
    def items(self):
        if self._len <= self.perPage:
            return self._items
        else:
            return self._items[int((self.currentPage-1)*self.perPage):int(self.currentPage*self.perPage)]

    @property
    def hasPrev(self):
        return self.currentPage >= 2

    @property
    def hasNext(self):
        if (self._len > self.perPage):
            return self.currentPage < (self._len/self.perPage)+1
        else:
            return self.currentPage < (self._len/self.perPage)

    def listPages(self, leftPadding=2, leftCurrent=2, rightPadding=2, rightCurrent=5):
        if (self._len > self.perPage):
            for num in range(1, (self._len/self.perPage)+2):
                if num <= leftPadding or \
                        (num > self.currentPage-leftPadding and \
                        num < self.currentPage + rightCurrent) or \
                        num > (self._len/self.perPage) - rightPadding:
                            yield num
        else:
            yield 1
