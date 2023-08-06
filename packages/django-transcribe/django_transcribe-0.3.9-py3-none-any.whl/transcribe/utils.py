import logging
from itertools import chain, islice, tee
from os import path

from transcribe import settings

# from transcribe import models

log = logging.getLogger(__name__)


def previous_and_next(an_iterable):
    prevs, items, nexts = tee(an_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


def convert_whitespace(str_with_whitespace, reverse=False):
    if reverse:
        rtn = str_with_whitespace.replace('NEWLINE', '\n').replace('TAB', '\t')
    else:
        rtn = (
            str_with_whitespace.replace('\n', 'NEWLINE')
            .replace('\t', 'TAB')
            .replace('<div>', 'NEWLINE')
            .replace('</div>', 'NEWLINE')
        )
    return rtn


def gen_diff_html(first_option, second_option):
    html_diff_pair = '<span class="opts">{}</span>'
    html_diff_first = '<span class="opt firstOption{empty}">{option}</span>'
    html_diff_second = '<span class="opt optHidden{empty}">{option}</span>'
    first = html_diff_first.format(
        empty=get_empty_class(first_option), option=' '.join(first_option)
    )
    second = html_diff_second.format(
        empty=get_empty_class(second_option), option=' '.join(second_option)
    )
    html = ''.join([first, second])
    return html_diff_pair.format(html)


def get_empty_class(option):
    return ' optEmpty' if is_empty_option(option) else ''


def is_empty_option(option):
    if option == []:
        return True
    elif len(option) == 1 and takes_no_space(option[0]):
        return True
    else:
        return False


def takes_no_space(text):
    """
    Returns True if all characters in `text` are non-printing
    characters, False otherwise.
    """
    if text == '':
        return True
    text = convert_whitespace(text, reverse=True)
    for character in text:
        if not is_non_printing(character):
            return False
    return True


def is_non_printing(character):
    """
    Returns True if `character` is a non-printing character. Currently,
    it only checks for newline characters.
    """
    return character in ['\n', '\r']


def root_path(*paths):
    return path.join(path.abspath(settings.BASE_DIR), *paths)
