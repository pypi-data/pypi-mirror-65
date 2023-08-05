import xml.etree.cElementTree as SVG


class Case:
    maxSpace = 6

    def __init__(self):
        self.space = 0
        self.shelfs = []
        self.space = 0

    def add(self, shelf):
        if self.space + 1 > self.maxSpace:
            return False
        else:
            self.shelfs.append(shelf)
            self.space = self.space + 1
            return True

    def draw(self, svg, position):
        left = position * 1050
        SVG.SubElement(svg, "rect",
                       fill="brown", stroke="#000",
                       x=str(left), y="500",
                       width="50", height="2000")
        SVG.SubElement(svg, "rect",
                       fill="brown", stroke="#000",
                       x=str(left + 1050), y="500",
                       width="50", height="2000")
        SVG.SubElement(svg, "rect",
                       fill="brown", stroke="#000",
                       x=str(left + 50), y="500",
                       width="1000", height="10")
        self.shelfIndex = 0
        left += 50
        self.shelfIndex = 0
        for shelf in self.shelfs:
            self.shelfIndex += 1
            shelf.draw(svg, left, self.shelfIndex)
