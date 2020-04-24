#!/usr/bin/env python

import os
import sys
import time
import datetime
import logging
import logging.config
import numpy as np

from inputs import argparser
from spectral_average_defaults import LOCATIONS
from spectral_average_defaults import LOGDIR, DEFAULT_RATE, DEFAULT_CUTOFF, DEFAULT_START, DEFAULT_SENSORS, DEFAULT_OUTDIR
from spectral_average_calc import spec_avg_date_range


def get_logger(log_file):

    # create logger
    logger = logging.getLogger('ugaudio')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs to DEBUG level
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # changed from ERROR to INFO

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_inputs(module_logger):

    # parse arguments
    module_logger.debug('parsing input arguments')
    args = argparser.parse_inputs()
    module_logger.info(str(args).replace('Namespace', 'Inputs: '))

    # adjust log level based on verbosity input args
    if args.quiet:
        module_logger.warning('Now switching to quiet for logging, that is, log level = WARNING.')
        level = logging.WARNING
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    # switch to same level for all handlers
    module_logger.setLevel(level)
    for handler in module_logger.handlers:
        handler.setLevel(level)

    return args


def main():

    # create logger
    log_file = os.path.join(LOGDIR, 'logs', 'ugaudio.log')
    module_logger = get_logger(log_file)
    module_logger.info('- STARTING MAIN UGAUDIO APP - -')
    module_logger.debug('log_file = %s' % log_file)

    # get input arguments
    args = get_inputs(module_logger)

    # for convenience in call below, let's rename args here
    pad_dir = args.paddir
    out_dir = args.outdir
    fs, fc = args.rate, args.cutoff
    day_start, day_stop = args.start, args.end
    nfft = args.nfft

    nfiles = args.nfiles

    # iterate over sensors
    daily_running_tallies = []
    for sensor in args.sensors:
        location = LOCATIONS[sensor]
        drt = spec_avg_date_range(sensor, location, day_start, day_stop, nfft, fs, fc, num_files=nfiles,
                                  pad_dir=pad_dir, out_dir=out_dir, do_plot=False)
        daily_running_tallies.append(drt)

    # iterate over daily running (spec avg) tallies
    for drt in daily_running_tallies:
        print drt

    return 0  # return zero for success, which is typical Linux command line behavior


if __name__ == '__main__':

    sys.exit(main())
