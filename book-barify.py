from collections import defaultdict
from sys import stdin
from typing import Tuple, List, Dict, Union
import bs4
import argparse
from argparse import ArgumentError
from csv import reader
from itertools import starmap
from math import inf
from re import compile as re_compile

formats = {
    'a3': (297, 420),
    'a4': (210, 297),
    'a5': (148, 210),
    '16:9': (1080, 1920),
    'dci': (2160, 4096),
    'cinemascope': (1000, 2350),
    'letter': (216, 279),
    'legal': (216, 356),
    'ledger': (279, 432),
}
custom_format_re = re_compile(r'([0-9]+)x([0-9]+)')


def page_format(spec: str) -> Tuple[int, int]:
    '''Type parser for the page format argument to the CLI.
    The page format can either be a pre-defined format from the list of formats (see above),
    or a format specification of the form WxH, where W and H are the width and height in millimeters, respectively.'''
    if spec in formats:
        return formats[spec]

    # parse WxH format
    if cf_spec := custom_format_re.match(spec):
        width_s, height_s = cf_spec.group(1), cf_spec.group(2)
        try:
            return int(width_s), int(height_s)
        except ValueError:
            raise ArgumentError(
                spec, 'width and height must be integers, but were {} and {}'.format(width_s, height_s))

    raise ArgumentError(
        spec, 'argument must be a predefined format {} or custom WxH format'.format(repr(formats.keys())))


def chapter_sizes(chapters_csv: List[str], color: str, sections: bool = False) -> List[Tuple[int, str, float, str]]:
    '''Parse the chapter sizes from a CSV file.
    The color argument is only used for the first "default" section or if there are no sections.
    Returns a list that contains the chapters,
    a tuple of the chapter number, name
    and the percentage length in comparison to the longest chapter
    and the color of this chapter.'''

    chapters_reader = reader(chapters_csv, delimiter=',')
    chapters_dict = defaultdict(lambda: ('', 1))
    min_chapter, max_chapter = inf, 0
    current_section_color = color
    for chapter_csv in chapters_reader:
        if sections and len(chapter_csv) > 3:
            [chapter_num, name, page, section_color, *_] = chapter_csv
            current_section_color = section_color
        else:
            [chapter_num, name, page, *_] = chapter_csv

        chapter_num, page = int(chapter_num), int(page)
        # set max and min chapter
        if chapter_num < min_chapter:
            min_chapter = chapter_num
        if chapter_num > max_chapter:
            max_chapter = chapter_num
        chapters_dict[chapter_num] = (name, page, color) if not sections else (
            name, page, current_section_color)

    chapters = []
    max_chapter_diff = 0
    for index in range(min_chapter, max_chapter+1):
        name, page, color = chapters_dict[index]
        # obtains name and page of previous chapter, can't fail b/c defaultdict
        _, page_prev, *_ = chapters_dict[index-1]
        # compute page difference and update maximum if necessary
        page_diff = page - page_prev
        if page_diff > max_chapter_diff:
            max_chapter_diff = page_diff
        chapters.append((index, name, page_diff, color))

    return list(starmap(lambda index, name, pages, ccolor: (index, name, float(pages) / max_chapter_diff, ccolor), chapters))


def mm(val) -> str:
    '''Helper function to convert any length to a millimeter value.'''
    return str(val) + 'mm'


def simple_bars(base: bs4.BeautifulSoup, img: bs4.element.Tag, chapters: List[Tuple[int, str, float, str]], width: float, margin_width: float, margin_height: float, rect_height: float, bar_margin: float) -> None:
    '''Simple bar generator, where each chapter is on a separate line.'''
    for index, _, clen, ccolor in chapters:
        rect_width = (width - 2*margin_width) * clen
        pos_y = margin_height + (index-1) * rect_height * 2
        crect = img.new_tag('rect',
                            x=mm(margin_width),
                            y=mm(pos_y),
                            height=mm(rect_height),
                            width=mm(rect_width),
                            style='fill:{};'.format(ccolor))
        base.append(crect)


def block_bars(base: bs4.BeautifulSoup, img: bs4.element.Tag, chapters: List[Tuple[int, str, float, str]], width: float, margin_width: float, margin_height: float, rect_height: float, bar_margin: float) -> None:
    '''Bar generator which creates an equal length of bar on each line, splitting up chapters over multiple lines in the process.'''
    drawsize_x = width - 2*margin_width
    # percentage x, line number y
    cur_x, cur_y = 0, 0
    for _, _, clen, ccolor in chapters:
        length_left = clen
        while length_left > 0:
            # --- draw one line based on this chapter

            end_x = cur_x + length_left
            if end_x > 1:
                # overshot the line end! draw until end of line
                percent_width = 1 - cur_x
            else:
                percent_width = length_left

            rect_width = drawsize_x * percent_width

            pos_x = margin_width + drawsize_x * cur_x
            pos_y = margin_height + cur_y * rect_height * 2
            crect = img.new_tag('rect',
                                x=mm(pos_x),
                                y=mm(pos_y),
                                height=mm(rect_height),
                                width=mm(rect_width),
                                style='fill:{};'.format(ccolor))
            base.append(crect)

            # update x and y
            cur_x += percent_width
            length_left -= percent_width
            if cur_x >= 1:
                cur_x = 0
                cur_y += 1
        # end while
        cur_x += bar_margin
        if cur_x > 1:
            cur_x = 0
            cur_y += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate bar images from book information',
                                     epilog='Copyright © 2021 kleines Filmröllchen. The MIT licence applies.', formatter_class=argparse.HelpFormatter)
    parser.add_argument('-i', '--input', required=True, action='store',
                        type=argparse.FileType('r', encoding='utf-8'), default=stdin,
                        help='File with book information, in CSV format: Chapter index, Chapter name, page number.')
    parser.add_argument('-o', '--output', required=True, action='store',
                        type=argparse.FileType('w', encoding='utf-8'), default=stdin,
                        help='Uutput SVG to write to. This SVG file is fully compliant and can be read with any browser.')

    parser.add_argument('-s', '--size', action='store',
                        type=page_format, default=formats['a4'],
                        help='The size of paper/screen to use. This can be selected from a set of standard sizes.')
    parser.add_argument('-f', '--flip', action='store_true', default=False,
                        help='Whether to flip the image, i.e. use landscape (wider than tall) mode.')

    parser.add_argument('-m', '--margin', action='store',
                        type=float, default=4.0,
                        help='Percentage margins to the edges.')
    parser.add_argument('-x', '--bar-margin', action='store',
                        type=float, default=0.02,
                        help='Percentage margins between bars on the same line. Used only by advanced bar layouts.')
    parser.add_argument('-r', '--rect-height', action='store', type=float,
                        help='Percentage height of each bar. This overrides automatic scaling.')
    parser.add_argument('-c', '--color', action='store',
                        type=str, default='black',
                        help='Color for the rectangles. Any HTML color is allowed but not checked by the script.')

    parser.add_argument('-a', '--sections', action='store_true', default=False,
                        help='Enable advanced coloring mode. In this mode, the fourth column can be used to introduce an HTML section color that is used as long as no more section color is found.')
    parser.add_argument('-b', '--block-mode', action='store_true', default=False,
                        help='Enable block mode bar image. On each line, there will be an equal length of bar on each line, splitting up chapters over multiple lines.')

    # --- argument processing
    args = parser.parse_args()
    width, height = args.size
    if args.flip:
        width, height = height, width
    margin_width = width * args.margin / 100.0
    margin_height = height * args.margin / 100.0
    input_lines = args.input.readlines()
    chapters = chapter_sizes(input_lines, args.color, args.sections)
    # (auto-)scaling
    if args.rect_height:
        rect_height = height * args.rect_height / 100.0
    elif not args.block_mode:
        rect_height = (height - margin_height * 2) / (len(chapters)*2)
    else:
        rect_height = (height - margin_height * 2) / (
            (sum(starmap(lambda _a, _b, clen, _c: clen, chapters)) +
             len(chapters) * args.bar_margin)
            * 2 + 1)

    # --- svg creation
    img = bs4.BeautifulSoup(features='xml')
    base = img.new_tag('svg', xmlns='http://www.w3.org/2000/svg',
                       width=mm(width), height=mm(height))
    img.append(base)

    if args.block_mode:
        block_bars(base, img, chapters, width,
                   margin_width, margin_height, rect_height, args.bar_margin)
    else:
        simple_bars(base, img, chapters, width,
                    margin_width, margin_height, rect_height, args.bar_margin)

    args.output.write(str(img))
