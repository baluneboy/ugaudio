#!/usr/bin/env python

import pandas as pd
from collections import deque
from dateutil import parser
from dateutil.relativedelta import relativedelta


i4 = pd.Interval(0, 1, closed='both')
i5 = pd.Interval(1, 2, closed='left')
print(i4)
print(i5)
print(i4.overlaps(i5))
raise SystemExit


def simple_demo():

    start_str = '2019-02-01'
    stop_str = '2019-02-03'

    # get files for all of start_str's PREVIOUS day
    start_day = parser.parse(start_str).replace(hour=0, minute=0, second=0, microsecond=0)
    prev_day = start_day - relativedelta(days=1)
    print(prev_day.strftime('%Y-%m-%d'), '<< get prev_day files before iteration begins')

    # FIXME sort prev_day files list

    # FIXME sort each day's files list before extending deque

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


if __name__ == '__main__':
    simple_demo()
