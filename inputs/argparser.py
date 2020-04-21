#!/usr/bin/env python

"""This module utilizes argparse from the standard library to define what arguments are required and handles those with
defaults and logic to help detect avoid invalid arguments."""


import os
import re
import logging
import argparse
from dateutil import parser as dparser

from ugaudio.defaults import DEFAULT_OUTDIR
from ugaudio.defaults import DEFAULT_SENSORS, DEFAULT_RATE, DEFAULT_CUTOFF
from ugaudio.defaults import DEFAULT_START

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


def start_str(t):
    """ return string provided only if it is a valid time at least 30 minutes from now

    :param t: string for time to start
    :return: string for time to start
    """
    return dparser.parse(t)


def sensor_str(s):
    """return string provided only if it is a valid esXX"""
    # TODO agree on consistent convention of string to refer to sensor (e.g. es09 or tshes-13); which is most prevalent?
    pat = re.compile(r'es\d{2}$', re.IGNORECASE)
    if re.match(pat, s):
        return s.lower()
    else:
        raise argparse.ArgumentError('"%s" does not appear to be a valid string for a TSH (e.g. es09)')


def parse_inputs():
    """parse input arguments using argparse from standard library"""

    parser = argparse.ArgumentParser(description="Command line argument handler for ugaudio project's main program.")

    # a group of args for verbosity
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true')
    group.add_argument('-q', '--quiet', action='store_true')

    # sample rate
    help_rate = "sample rate (sa/sec); default = %s" % str(DEFAULT_RATE)
    parser.add_argument('-r', '--rate', default=DEFAULT_RATE, type=rate_str, help=help_rate)

    # cutoff
    help_cutoff = "cutoff; default = %s" % str(DEFAULT_CUTOFF)
    parser.add_argument('-g', '--gain', default=DEFAULT_CUTOFF, type=cutoff_str, help=help_cutoff)

    # sensor
    # help_sensor = "sensor; default is %s" % DEFAULT_SENSOR
    # parser.add_argument('-s', '--sensor', default=DEFAULT_SENSOR, type=sensor_str, help=help_sensor)

    # output directory
    help_outdir = 'output dir; default is %s' % DEFAULT_OUTDIR
    parser.add_argument('-o', '--outdir', default=DEFAULT_OUTDIR, type=outdir_str, help=help_outdir)

    # start time
    help_start = 'start time; default is %s' % DEFAULT_START
    parser.add_argument('-t', '--start', default=DEFAULT_START, type=start_str, help=help_start)

    # FIXME we do not check that log directory seen in log_conf_file matches relative to outdir, assumed this above

    # parse arguments
    module_logger.debug('calling parse_args')
    args = parser.parse_args()

    return args
