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
        """
        :param items: a `list` of the items which are being paginated
        :param perPage: How many items to display per page
        :param currentPage: The page which is currently being displayed
        """
        self._items = items
        self.perPage = perPage
        self.currentPage = currentPage
        self._len = len(items)

    @property
    def items(self):
        """
        :prop items: Returns a `list` of the items, truncated at the correct place
            for pagination
        """
        if self._len <= self.perPage:
            return self._items
        else:
            return self._items[int((self.currentPage-1)*self.perPage):int(self.currentPage*self.perPage)]

    @property
    def hasPrev(self):
        """
        :prop hasPrev: Returns `True` or `False` depending on if there is a previous
            page or not.
        """
        return self.currentPage >= 2

    @property
    def hasNext(self):
        """
        :prop hasNext: Returns `True` or `False` depending on if there is a next
            page that can be displayed or not
        """
        if (self._len > self.perPage):
            return self.currentPage < (self._len/self.perPage)+1
        else:
            return self.currentPage < (self._len/self.perPage)

    def listPages(self, leftPadding=2, rightPadding=2, rightCurrent=5):
        """
        Yields a list of numbers which corrispond to the pages which are
        available to view

        :param leftPadding: The number of numbers less than the current page
            to return
        :param rightPadding: The number of numbers greater than the current
            page to return
        :param rightCurrent: The to go to, until we start getting past 1,2,3,etc
        """
        if (self._len > self.perPage):
            for num in range(1, (self._len/self.perPage)+2):
                if num <= leftPadding or \
                        (num > self.currentPage-leftPadding and \
                        num < self.currentPage + rightCurrent) or \
                        num > (self._len/self.perPage) - rightPadding:
                            yield num
        else:
            yield 1
