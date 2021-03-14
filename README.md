# book-barify
Turn your favorite books into informative bar images!

This script can create "bar images" from books, or rather information about the books. The most basic form is a series of horizontal bars, where each bar represents one chapter, with the relative length of the bars representing the chapter length. There may be further customizations to this in the future. This is an easy and automated way to visualize any book or other data in this form.

This script utilizes BeautifulSoup 4 for generating the SVG XML.

Help output:
```
usage: book-barify.py [-h] -i INPUT -o OUTPUT [-s {a3,a4,a5,16:9,dci,cinemascope,letter,legal,ledger}] [-f]
                      [-m MARGIN] [-r RECT_HEIGHT] [-c COLOR] [-a]

Generate bar images from book information

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File with book information, in CSV format: Chapter index, Chapter name, page number.
  -o OUTPUT, --output OUTPUT
                        Uutput SVG to write to. This SVG file is fully compliant and can be read with any browser.
  -s {a3,a4,a5,16:9,dci,cinemascope,letter,legal,ledger}, --size {a3,a4,a5,16:9,dci,cinemascope,letter,legal,ledger}
                        The size of paper/screen to use. This can be selected from a set of standard sizes.
  -f, --flip            Whether to flip the image, i.e. use landscape (wider than tall) mode.
  -m MARGIN, --margin MARGIN
                        Percentage margins to the edges.
  -r RECT_HEIGHT, --rect-height RECT_HEIGHT
                        Percentage height of each bar. This overrides automatic scaling.
  -c COLOR, --color COLOR
                        Color for the rectangles. Any HTML color is allowed but not checked by the script.
  -a, --sections        Enable advanced coloring mode. In this mode, the fourth column can be used to introduce an
                        HTML section color that is used as long as no more section color is found.

Copyright © 2021 kleines Filmröllchen. The MIT licence applies.
```

The aa_1.csv file is an example input file that supports the section mode. It contains the chapter info for "Alea Aquarius: Der Ruf des Wassers", a popular German children's novel, as well as the author's attempt at splitting the book into three acts (green: Act 1, blue: Act 2, red: Act 3).
