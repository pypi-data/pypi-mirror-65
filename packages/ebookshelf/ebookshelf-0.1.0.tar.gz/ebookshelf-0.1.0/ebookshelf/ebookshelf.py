#! /usr/bin/env python3
from .__init__ import __version__
import xml.etree.ElementTree as ET
from .book import Book
from .library import Library
import argparse

def main():

    parser = argparse.ArgumentParser(prog='ebookshelf',
                                     description="Takes an XML file from calibre, and draws a bookshelf.svg, that is linked to all eBooks")
    parser.add_argument('calibrefile',
                    help='filename of the XML file from Calibre')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__ ,
                        help='show the versionnumber and exit')
    parser.add_argument('--verbose', '-v',
                        action='count',
                        default=0)
    args = parser.parse_args()

    
    
    
    tree = ET.parse(args.calibrefile)
    
    books=[]
    for record in tree.getroot():
       books.append(Book(record))

    library=Library()
    for book in books:
        library.add(book)

    library.finalize()
    library.draw()
    
if __name__ == '__main__':
    main()
