#!/usr/bin/env python

"""
Explore...

"Fall in love with some activity, and do it! Nobody ever figures out what life
is all about, and it doesn't matter. Explore the world. Nearly everything is
really interesting if you go into it deeply enough. Work as hard and as much as
you want to on the things you like to do the best. Don't think about what you
want to be, but what you want to do. Keep up some kind of a minimum with other
things so that society doesn't stop you from doing anything at all."
- Richard P. Feynman

"""

import os
import datetime                   
from dateutil import parser       # convert string to datetime object
from scipy.io import loadmat      # this is the SciPy module that loads mat-files
import numpy as np                # support for large, multi-dimensional arrays and
                                  # matrices, plus high-level mathematical functions
import pandas as pd               # flexible & expressive data structures to work
                                  # with labeled data & pivot tables like in Excel
import matplotlib.pyplot as plt   # plotting similar to MATLAB
import matplotlib.dates as mdates

from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from pandas import Series, DataFrame
from datetime import datetime, timedelta


def read_astro_pi_csv():
    df = pd.read_csv('/misc/yoda/www/plots/user/socorro/astropi/Node2_Izzy_astro_pi_datalog.csv')
    df['time'] = pd.to_datetime(df['time_stamp'])
    #df1 = df[df.time > pd.datetime(2016, 3, 10)]
    #df_subset = df1[df1.time < pd.datetime(2016, 3, 14)]
    #print df_subset
    return df


def convert_matlab_serialdatenum_to_datetime(matlab_datenum):
    return datetime.datetime.fromordinal(int(matlab_datenum) - 366) + datetime.timedelta(days=matlab_datenum%1)
    

def convert_matfile_to_csvfiles():
    mat_file = '/misc/yoda/www/plots/user/socorro/astropi/saw_angles_2016_03_10_00_00_00.mat';
    mat = loadmat(mat_file)    # load mat-file
    mdata = mat['saw_angles']  # struct variable in mat file
    mdtype = mdata.dtype       # dtypes of structures are "unsized objects"    
    ndata = {n: mdata[n][0, 0] for n in mdtype.names}
    
    # reconstruct the columns of the data
    columns = list(ndata['BGA'].dtype.names)
    
    # iterate over solar array (columns) to write CSV file for each
    for c in columns:
        arr = ndata['BGA'][c][0][0]
        print c
        df = pd.DataFrame(arr, columns=['GMT', 'Angle_deg'])
        df['GMT'] = df['GMT'].apply(convert_matlab_serialdatenum_to_datetime)
        df.to_csv('/misc/yoda/www/plots/user/socorro/astropi/angles%s.csv' % c, index=False)
        print '----'


def plot_angles_from_csv_file(fnames):
    
    majorLocator = MultipleLocator(12)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(2)
        
    fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True)
    
    alldays = DayLocator()

    date1 = datetime.datetime(2016, 3, 10)
    date2 = datetime.datetime(2016, 3, 14)
    delta = datetime.timedelta(hours=24)
    dates = drange(date1, date2, delta)

    dfs = []
    for fname in fnames:
        df = pd.read_csv(fname)
        dfs.append(df)
    
    # FIXME quick kludge for getting timing wrangled between data sets
    if os.path.basename(fnames[0]).startswith('anglesS'):
        dfs[3] = dfs[3].reindex(index=dfs[3].index.union(dfs[2].index).union(dfs[1].index).union(dfs[0].index))
    elif os.path.basename(fnames[0]).startswith('anglesP'):
        dfs[0] = dfs[0].reindex(index=dfs[0].index.union(dfs[2].index).union(dfs[1].index).union(dfs[3].index))
    else:
        raise Exception('unexpected basename for CSV file')
    
    dfs[0].plot(ax=ax[0], x='GMT', y='Angle_deg')
    dfs[1].plot(ax=ax[1], x='GMT', y='Angle_deg')
    dfs[2].plot(ax=ax[2], x='GMT', y='Angle_deg')
    dfs[3].plot(ax=ax[3], x='GMT', y='Angle_deg')
    
    # set common labels
    for a in ax:
        a.set_ylabel('Angle (deg.)')
        a.legend().set_visible(False)
        print a.get_xlim()


    ax[3].set_xlabel('GMT')
        
    plt.show()


def build_fname(csv_path, side, part):
    bname = 'angles%s%s.csv' % (side, part)
    return os.path.join(csv_path, bname)
    
def demo():
    
    idx = pd.date_range('2011-05-01', '2011-07-01')
    s = pd.Series(np.random.randn(len(idx)), index=idx)
    
    fig, ax = plt.subplots()
    ax.plot_date(idx.to_pydatetime(), s, 'v-')
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(1),
                                                    interval=1))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))
    ax.xaxis.grid(True, which="minor")
    ax.yaxis.grid()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('\n\n\n%b\n%Y'))
    plt.tight_layout()
    plt.show()


def rolling_mean(data, window, min_periods=1, center=False):
    ''' Function that computes a rolling mean

    Parameters
    ----------
    data : DataFrame or Series
           If a DataFrame is passed, the rolling_mean is computed for all columns.
    window : int or string
             If int is passed, window is the number of observations used for calculating 
             the statistic, as defined by the function pd.rolling_mean()
             If a string is passed, it must be a frequency string, e.g. '90S'. This is
             internally converted into a DateOffset object, representing the window size.
    min_periods : int
                  Minimum number of observations in window required to have a value.

    Returns
    -------
    Series or DataFrame, if more than one column    
    '''
    def f(x):
        '''Function to apply that actually computes the rolling mean'''
        if center == False:
            dslice = col[x-pd.tseries.frequencies.to_offset(window).delta+timedelta(0,0,1):x]
                # adding a microsecond because when slicing with labels start and endpoint
                # are inclusive
        else:
            dslice = col[x-pd.tseries.frequencies.to_offset(window).delta/2+timedelta(0,0,1):
                         x+pd.tseries.frequencies.to_offset(window).delta/2]            
        if dslice.size < min_periods:
            return np.nan
        else:
            return dslice.mean()

    data = DataFrame(data.copy())
    dfout = DataFrame()
    if isinstance(window, int):
        dfout = data.rolling(min_periods=min_periods, window=window, center=center).mean()
    elif isinstance(window, basestring):
        idx = Series(data.index.to_pydatetime(), index=data.index)
        for colname, col in data.iteritems():
            result = idx.apply(f)
            result.name = colname
            dfout = dfout.join(result, how='outer')
    if dfout.columns.size == 1:
        dfout = dfout.ix[:,0]
    return dfout


def example():
    # Example
    idx = [datetime(2011, 2, 7, 0, 0),
           datetime(2011, 2, 7, 0, 1),
           datetime(2011, 2, 7, 0, 2),
           datetime(2011, 2, 7, 0, 3),
           datetime(2011, 2, 7, 0, 4),
           datetime(2011, 2, 7, 0, 5),
           datetime(2011, 2, 7, 0, 6),
           #datetime(2011, 2, 7, 0, 7),
           #datetime(2011, 2, 7, 0, 8),
           datetime(2011, 2, 7, 0, 9)]
    idx = pd.Index(idx)
    vals = np.arange(len(idx)).astype(float)
    s = Series(vals, index=idx)
    print s
    rm = rolling_mean(s, window='5min')
    print rm


def example2():
    csv_file = '/misc/yoda/www/plots/user/socorro/astropi/Node2_Izzy_astro_pi_datalog.csv'
    df = pd.read_csv(csv_file);
    print len(df)
    df['t'] = np.arange(0, 1127700, 10)
    df['accel_v'] = np.sqrt(df.accel_x**2 + df.accel_y**2 + df.accel_z**2);
    #rm = rolling_mean(df['accel_v'], window='32sec')
    df.plot(x='t', y='accel_v')
    plt.show()
    

if __name__ == '__main__':
    
    example2()
    raise SystemExit

    #demo()
    #raise SystemExit
    
    ## load astropi (izzy) csv file into pandas data structure
    #df = read_astro_pi_csv()

    ## convert MATLAB file (from JSC) to CSV files for ease of use
    #convert_matfile_to_csvfiles()

    # plot angles from CSV file
    csv_path = '/misc/yoda/www/plots/user/socorro/astropi'  # path to angle CSV files
    for side in ['P', 'S']:
        four_parts = ['IL', 'IU', 'OL', 'OU']
        fnames = [build_fname(csv_path, side, p) for p in four_parts]
        plot_angles_from_csv_file(fnames)
