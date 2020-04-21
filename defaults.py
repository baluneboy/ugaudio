import os
import datetime

LOCATIONS = {
        # SENSOR   LOCATION
        '121f02':  'JPM1A6, RMS Console, Seat Track',
        '121f03':  'LAB1O1, ER2, Lower Z Panel',
        '121f04':  'LAB1P2, ER7, Cold Atom Lab Front Panel',
        '121f05':  'JPM1F1, ER5, Inside RTS/D2',
        '121f08':  'COL1A3, EPM, near PK-4',
}

# TODO figure out what makes sense to have defaults for (or not) -- this should be happening as we develop

LOGDIR = 'C:/temp'  # parent directory for logs folder

DEFAULT_RATE = 500.0  # samples/second
DEFAULT_CUTOFF = 200.0  # Hz
DEFAULT_START = str(datetime.datetime.now().date() - datetime.timedelta(days=2))  # start date (TWODAYSAGO)
DEFAULT_OUTDIR = 'c:/temp' if os.name == 'nt' else '/tmp'  # results/output directory
DEFAULT_SENSORS = [k for k in LOCATIONS.keys()]
DEFAULT_SENSORS.sort()
