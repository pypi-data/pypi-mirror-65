from __future__ import print_function

import math
import random
import re
import sys

PY3 = sys.version_info >= (3,)

STRIP_ANSI = re.compile(r'\x1b\[(\d+)(;\d+)?(;\d+)?[m|K]')
COLOR_ANSI = (
    (0x00, 0x00, 0x00), (0xcd, 0x00, 0x00),
    (0x00, 0xcd, 0x00), (0xcd, 0xcd, 0x00),
    (0x00, 0x00, 0xee), (0xcd, 0x00, 0xcd),
    (0x00, 0xcd, 0xcd), (0xe5, 0xe5, 0xe5),
    (0x7f, 0x7f, 0x7f), (0xff, 0x00, 0x00),
    (0x00, 0xff, 0x00), (0xff, 0xff, 0x00),
    (0x5c, 0x5c, 0xff), (0xff, 0x00, 0xff),
    (0x00, 0xff, 0xff), (0xff, 0xff, 0xff),
)


class LolCat(object):
    text: str

    def __init__(self, mode=256, output=sys.stdout):
        self.mode = mode
        self.output = output

    def _distance(self, rgb1, rgb2):
        return sum(map(lambda c: (c[0] - c[1]) ** 2,
                       zip(rgb1, rgb2)))

    def ansi(self, rgb):
        r, g, b = rgb

        if self.mode in (8, 16):
            colors = COLOR_ANSI[:self.mode]
            matches = [(self._distance(c, map(int, rgb)), i) for i, c in enumerate(colors)]
            matches.sort()
            color = matches[0][1]

            return '3%d' % (color,)
        else:
            gray_possible = True
            sep = 2.5

            while gray_possible:
                if r < sep or g < sep or b < sep:
                    gray = r < sep and g < sep and b < sep
                    gray_possible = False

                sep += 42.5

            if gray:
                color = 232 + int(float(sum(rgb) / 33.0))
            else:
                color = sum([16] + [int(6 * float(val) / 256) * mod
                                    for val, mod in zip(rgb, [36, 6, 1])])

            return '38;5;%d' % (color,)

    def wrap(self, *codes):
        return '\x1b[%sm' % (''.join(codes),)

    def rainbow(self, freq, i):
        r = math.sin(freq * i) * 127 + 128
        g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
        b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
        return [r, g, b]

    def cat(self, fd, options):
        self.text = ""
        for line in fd:
            options["os"] += 1
            self.println(line, options)
        return self.text

    def println(self, s, options):
        if self.output.isatty():
            s = STRIP_ANSI.sub('', s)

        self.println_plain(s, options)

    def println_plain(self, s, options):
        for i, c in enumerate(s if PY3 else s.decode(options['charset_py2'], 'replace')):
            rgb = self.rainbow(options['freq'], options['os'] + i / options['spread'])
            self.text += (''.join([
                self.wrap(self.ansi(rgb)),
                c if PY3 else c.encode(options['charset_py2'], 'replace'),
            ]))


def lolcat(str):
    options = {'spread': 1.0, 'freq': 0.1, 'seed': 0, 'animate': False, 'duration': 12, 'speed': 20.0, 'force': False,
               'mode': None, 'charset_py2': 'utf-8', 'os': random.randint(0, 256)}

    lolcat = LolCat()
    text = lolcat.cat(str, options)
    del lolcat
    return text
