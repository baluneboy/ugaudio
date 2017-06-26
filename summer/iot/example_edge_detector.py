#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO  

INPUT_PIN = 18 

GPIO.setmode(GPIO.BCM)                                     # set up BCM GPIO numbering  
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # set as input
 
# Define a threaded callback function to run in another thread when events are detected  
def OLDmy_callback(channel):  
    if GPIO.input(INPUT_PIN): # if port INPUT_PIN == 1  
        print "Rising edge detected on INPUT_PIN"  
    else:                     # if port INPUT_PIN != 1  
        print "Falling edge detected on INPUT_PIN"  
  
# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel):  
    sleep(0.25)
    value = GPIO.input(INPUT_PIN)
    if value == 1: # if INPUT_PIN went HIGH
        print "Rising edge detected on INPUT_PIN"  
    else:          # if INPUT_PIN went LOW
        print "Falling edge detected on INPUT_PIN"  

# when a changing edge is detected on port INPUT_PIN, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(INPUT_PIN, GPIO.BOTH, callback=my_callback, bouncetime=300)  

print "Program will finish after 30 seconds or if you press CTRL+C\n"  
print "Make sure you have a button connected, pulled down through 10k resistor"  
print "to GND and wired so that when pressed it connects"  
print "GPIO port INPUT_PIN to 3V3 GND (pin 6) through a ~5k resistor\n"  
  
print "Also put a 100 nF capacitor across your switch for hardware debouncing"  
print "This is necessary to see the effect we're looking for"  
raw_input("Press Enter when ready\n>")  
  
try:  
    print "When pressed, you'll see: Rising Edge detected on INPUT_PIN"  
    print "When released, you'll see: Falling Edge detected on INPUT_PIN"  
    sleep(35)         # wait
    print "Time's up. Finished!"  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  
