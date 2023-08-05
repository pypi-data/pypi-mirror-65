import xml.etree.cElementTree as SVG
from math import sqrt
import random
import hashlib


class Book:

    maxPages = 0

    def __init__(self, booknode):
        self.publisher = "None"
        self.series = "None"
        self.authors = []
        for el in booknode:
            if el.tag == "_genre":
                self.genre = el.text
            elif el.tag == "_seiten":
                self.pages = int(el.text)
                if self.pages > Book.maxPages:
                    Book.maxPages = self.pages
            elif el.tag == "_worte":
                if el.text == "None":
                    self.words = 0
                else:
                    self.words = int(el.text)
            elif el.tag == "id":
                self.bookId = el.text
            elif el.tag == "uuid":
                self.uuid = el.text
            elif el.tag == "size":
                self.size = int(el.text)
            elif el.tag == "title":
                self.title = el.text
            elif el.tag == "library_name":
                self.library = el.text
            elif el.tag == "timestamp":
                self.timestamp = el.text
            elif el.tag == "pubdate":
                self.pubdate = el.text
            elif el.tag == "publisher":
                self.publisher = el.text
            elif el.tag == "isbn":
                self.isbn = el.text
            elif el.tag == "rating":
                self.rating = el.text
            elif el.tag == "series":
                self.series = el.text
            elif el.tag == "comments":
                self.comments = el.text
            elif el.tag == "cover":
                self.cover = el.text
            elif el.tag == "identifiers":
                self.identifiers = el.text
            elif el.tag == "tags":
                self.tags = []
            elif el.tag == "formats":
                self.formats = []
                for format in el:
                    self.formats.append(format.text)
            elif el.tag == "authors":
                for author in el:
                    self.authors.append(author.text)
            else:
                print(el.tag)

    def shelfspace(self):
        return sqrt(1-(1-(self.pages / Book.maxPages) ** 2)) * 90 + 10

    def draw(self, svg, bottom, position):
        hex = hashlib.md5(self.publisher.encode('utf-8')).hexdigest()
        h = int(int("0x" + str(hex)[-2:], 16)/2)
        col = "#" + str(hex)[-6:]
        pubcol = "#" + str(hex)[-8:-2]
        hex = hashlib.md5(self.series.encode('utf-8')).hexdigest()
        sercol = "#" + str(hex)[-8:-2]

        link = SVG.SubElement(svg, "a",
                              href=self.formats[0],
                              type="application/epub+zip")

        linktitle = SVG.SubElement(link, "title")
        linktitle.text = self.title

        book = SVG.SubElement(link, "rect",
                              fill=col,
                              stroke="black",
                              x=str(position),
                              y=str(bottom-192-h),
                              width=str(self.shelfspace()),
                              height=str(192+h))
        book.set("stroke-width", "0.5")

        publisher = SVG.SubElement(link, "rect",
                                   fill=pubcol,
                                   stroke="black",
                                   x=str(position),
                                   y=str(bottom-16),
                                   width=str(self.shelfspace()),
                                   height=str(16))
        publisher.set("stroke-width", "0.5")

        series = SVG.SubElement(link, "rect",
                                fill=sercol,
                                stroke="black",
                                x=str(position),
                                y=str(bottom - 192 - h),
                                width=str(self.shelfspace()),
                                height=str(16))
        series.set("stroke-width", "0.5")

        title = SVG.SubElement(link, "text",
                               x=str(position + self.shelfspace()/2 + 4),
                               y=str(bottom - 170 - h))
        title.set("stroke-width", "0.5")
        title.set("transform",
                  "rotate(-90 " + str(position+self.shelfspace()/2 + 4) +
                  " " + str(bottom - 170 - h) + ")")
        title.set("stroke", "white")
        title.set("text-anchor", "end")
        title.set("font-family", "Arial")
        title.set("font-size", "10")
        title.set("fill", "white")
        title.text = self.title[:30]

        author = SVG.SubElement(link, "text",
                                x=str(position+self.shelfspace()/2 + 4),
                                y=str(bottom-16))
        author.set("stroke-width", "0.5")
        author.set("transform",
                   "rotate(-90 " + str(position+self.shelfspace()/2 + 4) +
                   " " + str(bottom-16)+")")
        author.set("stroke", "white")
        author.set("text-anchor", "start")
        author.set("font-family", "Arial")
        author.set("font-size", "5")
        author.set("fill", "white")
        author.text = self.authors[0][:30]
