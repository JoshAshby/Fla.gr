
class pagination(object):
    def __init__(self, items, perPage, currentPage):
        self.items = items
        self.perPage = perPage
        self.currentPage = currentPage
        self.itemLen = len(items)

    @property
    def getItems(self):
        if self.itemLen <= self.perPage:
            return self.items
        else:
            return self.items[int((self.currentPage-1)*self.perPage):int(self.currentPage*self.perPage)]

    @property
    def hasPrev(self):
        return self.currentPage >= 2

    @property
    def hasNext(self):
        if (self.itemLen > self.perPage):
            return self.currentPage < (self.itemLen/self.perPage)+1
        else:
            return self.currentPage < (self.itemLen/self.perPage)

    def listPages(self, leftPadding=2, leftCurrent=2, rightPadding=2, rightCurrent=5):
        if (self.itemLen > self.perPage):
            for num in range(1, (self.itemLen/self.perPage)+2):
                if num <= leftPadding or \
                        (num > self.currentPage-leftPadding and \
                        num < self.currentPage + rightCurrent) or \
                        num > (self.itemLen/self.perPage) - rightPadding:
                            yield num
        else:
            yield 1
