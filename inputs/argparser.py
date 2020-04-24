#!/usr/bin/env python

"""This module utilizes argparse from the standard library to define what arguments are required and handles those with
defaults and logic to help detect avoid invalid arguments."""


import os
import re
import logging
import argparse
from dateutil import parser as dparser
from pims.signal.rounding import is_power_of_two

from defaults import DEFAULT_OUTDIR, DEFAULT_PADDIR
from defaults import DEFAULT_SENSORS, DEFAULT_RATE, DEFAULT_CUTOFF, DEFAULT_NFFT, DEFAULT_NFILES
from defaults import DEFAULT_START, DEFAULT_END

# create logger
module_logger = logging.getLogger('ugaudio.argparser')


def folder_str(f):
    """return string provided only if this folder exists"""
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError('"%s" does not exist, you must create this folder' % f)
    return f


def outdir_str(d):
    """return string provided only if this folder exists and we can create logs subdir in it"""
    f = folder_str(d)
    logs_dir = os.path.join(f, 'logs')
    try:
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
    except OSError:
        raise argparse.ArgumentTypeError('could not create "%s" directory' % logs_dir)
    return f


def nfiles_int(n):
    """return valid num_files as int value converted from string, n"""
    try:
        value = int(n)
    except Exception as e:
        raise argparse.ArgumentTypeError('%s' % e)
    return value


def nfft_int(n):
    """return valid Nfft as int value converted from string, n"""
    try:
        value = int(n)
    except Exception as e:
        raise argparse.ArgumentTypeError('%s' % e)

    # FIXME this is serious hard-coded kludge for now until we can make this more robust
    if not is_power_of_two(value):
        raise argparse.ArgumentTypeError('Nfft should really be power of two for now')

    return value


def rate_str(r):
    """return valid sample rate (sa/sec) as float value converted from string, r"""
    try:
        value = float(r)
    except Exception as e:
        raise argparse.ArgumentTypeError('%s' % e)

    # FIXME this is serious hard-coded kludge for now until we can make this more robust
    if value != 500.0:
        raise argparse.ArgumentTypeError('rate, r, in sa/sec must be 500.0 for now')

    return value


def cutoff_str(g):
    """return valid cutoff as float value converted from string, g"""
    try:
        value = float(g)
    except Exception as e:
        raise argparse.ArgumentTypeError('%s' % e)

    # FIXME this is serious hard-coded kludge for now until we can make this more robust
    if value != 200.0:
        raise argparse.ArgumentTypeError('rate, r, in sa/sec must be 200.0 for now')

    return value


def dtm_date(t):
    """ return string provided only if it is a valid date

    :param t: string for date to start
    :return: datetime.date object for start
    """
    return dparser.parse(t).date()


def sensors_list(s):
    """return list of strings"""
    slist = s.split(' ')
    pat = re.compile(r'es\d{2}$|121f\d{2}$', re.IGNORECASE)
    sensors = [se for se in slist if re.match(pat, se)]
    if len(sensors) == 0:
        raise argparse.ArgumentError('"%s" does not appear to contain any valid sensor strings (e.g. es09 or 121f02)')
    return sensors


def parse_inputs():
    """parse input arguments using argparse from standard library"""

    parser = argparse.ArgumentParser(description="Command line argument handler for ugaudio project's main program.")

    # a group of args for verbosity
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true')
    group.add_argument('-q', '--quiet', action='store_true')

    # nfiles
    help_nfiles = "nfiles to preview (for testing); default = %s" % str(DEFAULT_NFILES)
    parser.add_argument('-g', '--nfiles', default=DEFAULT_NFILES, type=nfiles_int, help=help_nfiles)

    # nfft
    help_nfft = "Nfft; default = %s" % str(DEFAULT_NFFT)
    parser.add_argument('-n', '--nfft', default=DEFAULT_NFFT, type=nfft_int, help=help_nfft)

    # sample rate
    help_rate = "sample rate (sa/sec); default = %s" % str(DEFAULT_RATE)
    parser.add_argument('-r', '--rate', default=DEFAULT_RATE, type=rate_str, help=help_rate)

    # cutoff
    help_cutoff = "cutoff; default = %s" % str(DEFAULT_CUTOFF)
    parser.add_argument('-c', '--cutoff', default=DEFAULT_CUTOFF, type=cutoff_str, help=help_cutoff)

    # sensors
    help_sensors = "sensors; default is %s" % DEFAULT_SENSORS
    parser.add_argument('-s', '--sensors', default=DEFAULT_SENSORS, type=sensors_list, help=help_sensors)

    # PAD directory
    help_paddir = 'PAD dir; default is %s' % DEFAULT_PADDIR
    parser.add_argument('-p', '--paddir', default=DEFAULT_PADDIR, type=folder_str, help=help_paddir)

    # output directory
    help_outdir = 'output dir; default is %s' % DEFAULT_OUTDIR
    parser.add_argument('-o', '--outdir', default=DEFAULT_OUTDIR, type=outdir_str, help=help_outdir)

    # start date
    help_start = 'start date; default is %s' % DEFAULT_START
    parser.add_argument('-t', '--start', default=DEFAULT_START, type=dtm_date, help=help_start)

    # end date
    help_end = 'end date; default is %s' % DEFAULT_END
    parser.add_argument('-e', '--end', default=DEFAULT_END, type=dtm_date, help=help_end)

    # parse arguments
    module_logger.debug('calling parse_args')
    args = parser.parse_args()

    return args
