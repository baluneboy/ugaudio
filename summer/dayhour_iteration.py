#!/usr/bin/env python

import numpy as np
import pandas as pd
from collections import deque
from dateutil import parser
from dateutil.relativedelta import relativedelta


# i4 = pd.Interval(0, 1, closed='both')
# i5 = pd.Interval(1, 2, closed='left')
# print(i4)
# print(i5)
# print(i4.overlaps(i5))
# raise SystemExit

a = np.arange(12).reshape(3, 4)
min_values = np.nanmin(a, axis=0)
max_values = np.nanmax(a, axis=0)
std_values = np.nanstd(a, axis=0)

min_str = '{:.2f},{:.2f},{:.2f}'.format(*min_values)
max_str = '{:.2f},{:.2f},{:.2f}'.format(*max_values)
std_str = '{:.2f},{:.2f},{:.2f}'.format(*std_values)
print('%s,%s,%s' % (min_str, max_str, std_str))

raise SystemExit


def simple_demo_fwd():

    start_str = '2019-02-01'
    stop_str = '2019-02-03'

    # FIXME sort each day's files list before extending deque

    # get files for all of start_str's PREVIOUS day
    start_day = parser.parse(start_str).replace(hour=0, minute=0, second=0, microsecond=0)
    prev_day = start_day - relativedelta(days=1)
    print(prev_day.strftime('%Y-%m-%d'), '<< get prev_day files before iteration begins')

    # get files for all of start_str's day
    print(start_day.strftime('%Y-%m-%d'), '<< get start_day files before iteration begins')

    # iterate from start_str's day/hour up to, but excluding stop_str's day/hour
    dhr = pd.date_range(start_str, stop_str, freq='1H')
    for dh in dhr[:-1]:

        # if it's high noon, then get list of matching files for next day and extend deque
        if dh.hour == 12:
            next_day = dh.replace(hour=0) + relativedelta(days=1)
            print(next_day.strftime('%Y-%m-%d'), '<< high noon, so extend deque with this next day files')

        # iterate over deque, popping only files that overlap Interval from dh:dh+relativedelta(hours=1)
        print(dh.strftime('%Y-%m-%d/%H'), 'extracted (v,x,y,z) data from files for this dh')


def simple_demo_rev():

    start_str = '2019-02-01'
    stop_str = '2019-02-03'

    # FIXME reverse sort each day's files list before extending deque

    # get files for all of stop_str's day
    stop_day = parser.parse(stop_str).replace(hour=0, minute=0, second=0, microsecond=0)
    prev_day = stop_day - relativedelta(days=1)
    print(stop_day.strftime('%Y-%m-%d'), '<< get stop_day files before iteration begins')

    # get files for all of start_str's day
    print(prev_day.strftime('%Y-%m-%d'), '<< get prev_day files before iteration begins')

    # iterate down from last dh of prev_day's day/hour down to, and including start_str's day/hour
    dhr = pd.date_range(start_str, stop_str, freq='1H')[:-1]
    for dh in dhr[::-1]:  # fancy indexing gets us the reversed chronological ordering

        # if it's high noon, then get list of matching files for prior day and extend deque
        if dh.hour == 12:
            prior_day = dh.replace(hour=0) - relativedelta(days=1)
            print(prior_day.strftime('%Y-%m-%d'), '<< high noon, so extend deque with prior day files')

        # iterate over deque, popping only files that overlap Interval from dh:dh+relativedelta(hours=1)
        print(dh.strftime('%Y-%m-%d/%H'), 'extracted (v,x,y,z) data from files for this dh')


if __name__ == '__main__':
    simple_demo_rev()
