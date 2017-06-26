#!/usr/bin/env python

import sys
import time
import datetime
import RPi.GPIO as gpio

def banger(duration):
    PIN_OUT = 18

    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_OUT, gpio.OUT)

    gpio.output(PIN_OUT, True)
    time.sleep(duration)
    gpio.output(PIN_OUT, False)

    gpio.cleanup()
    print 'done with banger'

def fan(duration):
    PIN_OUT = 23

    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_OUT, gpio.OUT)

    gpio.output(PIN_OUT, True)
    time.sleep(duration)
    gpio.output(PIN_OUT, False)

    gpio.cleanup()
    print 'done with fan'

def endlessly_monitor_mode_switch():
    PIN_IN = 4

    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_IN, gpio.IN)

    print 'endlessy monitoring mode switch (Ctrl-C to quit)'
    
    # initialize
    prev_input = gpio.input(PIN_IN)
    while True:

        # take a reading
        input = gpio.input(PIN_IN)

        # show when switch changes state
        if prev_input != input:
            print "Switched from %d to %d" % (prev_input, input)

        # update previous input
        prev_input = input

        # slight pause [do we need to debounce a toggle switch?]
        time.sleep(0.05)

def get_mode_switch():
    PIN_IN = 4
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_IN, gpio.IN)
    return gpio.input(PIN_IN)

def knock_five(spacing=[0, 0.3, 0.5, 0.6, 0.9]):
    PIN_OUT = 18

    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_OUT, gpio.OUT)

    for s in spacing:
        gpio.output(PIN_OUT, True)
        time.sleep(0.1)
        gpio.output(PIN_OUT, False)
        time.sleep(s)

    gpio.cleanup()
    print 'done with knock_five'
    
#knock_five()
#raise SystemExit
    
#endlessly_monitor_mode_switch()
#raise SystemExit

count = int( sys.argv[1] )
duration = float( sys.argv[2] )
mode = get_mode_switch()
for i in range(count):
    fan(duration)
    time.sleep(0.2)
    if mode:
        banger(duration)
        time.sleep(0.2)
