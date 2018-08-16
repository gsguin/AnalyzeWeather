# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:32:02 2018

@author: GG9323
"""

try:
    from itertools import izip_longest  # added in Py 2.6
except ImportError:
    from itertools import zip_longest as izip_longest  # name change in Py 3.x

try:
    from itertools import accumulate  # added in Py 3.2
except ImportError:
    def accumulate(iterable):
        'Return running totals (simplified version).'
        total = next(iterable)
        yield total
        for value in iterable:
            total += value
            yield total

def make_parser(fieldwidths):
    cuts = tuple(cut for cut in accumulate(abs(fw) for fw in fieldwidths))
    pads = tuple(fw < 0 for fw in fieldwidths) # bool values for padding fields
    flds = tuple(izip_longest(pads, (0,)+cuts, cuts))[:-1]  # ignore final one
    parse = lambda line: tuple(line[i:j] for pad, i, j in flds if not pad)
    # optional informational function attributes
    parse.size = sum(abs(fw) for fw in fieldwidths)
    parse.fmtstring = ' '.join('{}{}'.format(abs(fw), 'x' if fw < 0 else 's')
                                                for fw in fieldwidths)
    return parse

import datetime
import pandas as pd
import numpy as np

t_tmp=None

if not(t_tmp):
    t_tmp = 'abc'
else:
    t_tmp = 'bcd'
print(t_tmp)

todays_date = datetime.datetime.now().date()
index = pd.date_range(todays_date-datetime.timedelta(10), periods=10, freq='D')

columns = ['A','B', 'C']
df_ = pd.DataFrame(index=index, columns=columns)
df_ = df_.fillna(0)

line = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n'
fieldwidths = (2, -10, 24)  # negative widths represent ignored padding fields
parse = make_parser(fieldwidths)
fields = parse(line)
print('format: {!r}, rec size: {} chars'.format(parse.fmtstring, parse.size))
print('fields: {}'.format(fields))