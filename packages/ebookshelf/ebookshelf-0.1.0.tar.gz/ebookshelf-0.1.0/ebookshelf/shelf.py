import xml.etree.cElementTree as SVG


class Shelf:
    maxSpace = 1000

    def __init__(self):
        self.space = 0
        self.books = []

    def add(self, book):
        if book.shelfspace() + self.space > self.maxSpace:
            return False
        else:
            self.books.append(book)
            self.space = self.space + book.shelfspace()
            return True

    def draw(self, svg, left, position):
        top = 500+330*position
        self.bookIndex = 0
        SVG.SubElement(svg, "rect",
                       fill="brown",
                       stroke="#000",
                       x=str(left),
                       y=str(top),
                       width="1000",
                       height="10")
        self.bookIndex = 0
        for book in self.books:
            book.draw(svg, top, left + self.bookIndex)
            self.bookIndex += book.shelfspace()
