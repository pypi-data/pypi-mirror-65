# This Python file uses the following encoding: utf-8
from sys import stdout
import math


# global params def
BAR_CHARS_HOR = [u'', u'▏', u'▎', u'▍', u'▌', u'▋', u'▊', u'▉', u'█']
BAR_CHARS_ASCII = [''] + list(map(str, range(1, 10))) + ['#']
LABEL_SEPARATOR_STR = ': | '


def _bar_elements_available(bar_elements, encoding):
    try:
        for elem in bar_elements:
            elem.encode(encoding)
        return True
    except UnicodeEncodeError:
        return False


def _get_bar_elements():
    if _bar_elements_available(BAR_CHARS_HOR, stdout.encoding):
        return BAR_CHARS_HOR
    return BAR_CHARS_ASCII  # used as a fallback solution


def _calc_scaling(data, width):
    """Calculates scaling factor for bar and padding for categories"""
    str_len = max(len(x) for x in data)

    # remaining chars until width reached:
    remaining_width = width - len(LABEL_SEPARATOR_STR) - str_len

    max_entry = float(max(data.values()))
    scale_fac = max_entry / remaining_width

    return (str_len, scale_fac)


def barplot(data, width=60):
    """Print bar plot of categorical data to terminal"""
    bar_elems = _get_bar_elements()
    str_len, scale_fac = _calc_scaling(data, width)

    for entry in data:
        frac, whole = math.modf(data[entry] / scale_fac)
        frac_char_idx = int(frac * 100) / (len(bar_elems) - 2)

        print(u'{}{}{}{}'.format(
            entry.rjust(str_len),
            LABEL_SEPARATOR_STR,
            bar_elems[-1] * int(whole),
            bar_elems[frac_char_idx]))


if __name__ == '__main__':

    test_data = {
        'a': 10,
        'b': 50,
        'c': 35,
        'd': 5
    }

    barplot(test_data)
