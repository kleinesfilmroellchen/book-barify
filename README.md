# book-barify
Turn your favorite books into informative bar images!

<img src=example.svg width=300px></img>

This script can create "bar images" from books, or rather information about the books. The most basic form is a series of horizontal bars, where each bar represents one chapter, with the relative length of the bars representing the chapter length. There may be further customizations to this in the future. This is an easy and automated way to visualize any book or other data in this form.

This script utilizes BeautifulSoup 4 for generating the SVG XML.

Help output:
```
usage: book-barify.py [-h] -i INPUT -o OUTPUT [-b] [-t] [-s SIZE] [-l] [-m MARGIN] [-x BAR_MARGIN]
                      [-u ANNOTATION_WIDTH] [-r RECT_HEIGHT] [-c COLOR] [-f FONT] [-g FONT_SIZE]

Generate bar images from book information

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File with book information, in CSV format: Chapter index, Chapter name, page       
                        number.
  -o OUTPUT, --output OUTPUT
                        Uutput SVG to write to. This SVG file is fully compliant and can be read with any  
                        browser.
  -b, --block-mode      Enable block mode bar image. On each line, there will be an equal length of bar    
                        on each line, splitting up chapters over multiple lines.
  -t, --text-annotations
                        Enable text annotation mode. In this mode, the fourth column of each chapter       
                        specifies a text annotation for this chapter that is printed to the right of the   
                        chapter's starting line.
  -s SIZE, --size SIZE  The size of paper/screen to use. This can be selected from the standard sizes:     
                        {a3, a4, a5, 16:9, dci, cinemascope, letter, legal, ledger}. Alternatively, use a  
                        custom size of the form WxH with W as the width and H as the height. The sizes     
                        are all in millimeters, though this has only symbolic meaning.
  -l, --flip            Whether to flip the image, i.e. use landscape (wider than tall) mode. This is      
                        still applicable to custom sizes.
  -m MARGIN, --margin MARGIN
                        Percentage margins to the edges.
  -x BAR_MARGIN, --bar-margin BAR_MARGIN
                        Percentage margins between bars on the same line. Used only by advanced bar        
                        layouts.
  -u ANNOTATION_WIDTH, --annotation-width ANNOTATION_WIDTH
                        Width of the text annotation area. Should be adjusted to be large enough for any   
                        text that is draw. A percentage of the entire page's width. This parameter is      
                        ignored if text annotation mode is not active.
  -r RECT_HEIGHT, --rect-height RECT_HEIGHT
                        Percentage height of each bar. This overrides automatic scaling.
  -c COLOR, --color COLOR
                        Color for the rectangles. Any HTML color is allowed but not checked by the
                        script.
  -f FONT, --font FONT  Font for anything that includes text in the image. May be any valid CSS font       
                        string, so a number of fallback fonts are allowed.
  -g FONT_SIZE, --font-size FONT_SIZE
                        Size of text in the image. May be any valid CSS length, but avoid relative sizes.  

Copyright © 2021 kleines Filmröllchen. The MIT licence applies.
```

The example.csv file is an an example input file with colored sections based on *Alice in Wonderland*. The example.svg output file was generated without any options except input and output.
