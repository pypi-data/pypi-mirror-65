import os
import re
import string
import sys
from importlib.resources import read_text
from . import resources


def replace_bad_char(ex):
    return (u"?", ex.start)


class DefaultFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        try:
            return super().format_field(value, format_spec)
        except:
            return "" if value is None else str(value)


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, "sql", filename)


def read_file(filename):
    return read_text(resources, filename)


def add_table_border(text, border=1):
    lines = [(" " * border) + line for line in text.split("\n")]
    length = max([len(a) for a in lines])

    return "\n".join([l.ljust(length) for l in lines])


def regex_factory(regex):
    """Convenience wrapper around regex with named capture groups.
    """
    reg = re.compile(regex, re.I)

    def _match(text):
        m = reg.match(text)
        if m:
            return m.groupdict()
        return None

    return _match
