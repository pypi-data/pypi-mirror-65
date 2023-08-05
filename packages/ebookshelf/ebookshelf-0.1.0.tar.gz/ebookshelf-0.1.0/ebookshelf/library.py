import xml.etree.cElementTree as SVG

from .shelf import Shelf
from .case import Case


class Library:
    cases = []
    case = None
    shelf = None

    def add(self, book):
        if self.shelf is None:
            self.shelf = Shelf()
        if self.case is None:
            self.case = Case()
        if not self.shelf.add(book):
            if not self.case.add(self.shelf):
                self.cases.append(self.case)
                self.case = Case()
                self.case.add(self.shelf)
            self.shelf = Shelf()
            self.shelf.add(book)

    def caseCount(self):
        return len(self.cases)

    def finalize(self):
        if not self.case.add(self.shelf):
            self.cases.append(self.case)
            self.case = Case()
            self.case.add(self.shelf)
        self.cases.append(self.case)

    def draw(self):
        svg = SVG.Element("svg",
                          xmlns="http://www.w3.org/2000/svg",
                          id="Calibre Bookshelf",
                          version="2.0",
                          width=str(1050*(len(self.cases)+1)+50),
                          height="3000")
        caseIndex = 0
        for case in self.cases:
            case.draw(svg, caseIndex)
            caseIndex += 1

        tree = SVG.ElementTree(svg)
        tree.write("test.svg")
