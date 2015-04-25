#!/usr/bin/env python

"""explore...

"Fall in love with some activity, and do it! Nobody ever figures out what life
is all about, and it doesn't matter. Explore the world. Nearly everything is
really interesting if you go into it deeply enough. Work as hard and as much as
you want to on the things you like to do the best. Don't think about what you
want to be, but what you want to do. Keep up some kind of a minimum with other
things so that society doesn't stop you from doing anything at all."
- Richard P. Feynman

"""

import aifc
import pygame
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from ugaudio.create import aiffread
from ugaudio.signal import pitchshift, timearray

# TODO put more power to explore in user's hands!
# TODO import and [completely] process iSeismograph files?

def main():
    
    fps, bowl_sound = wavfile.read("/Users/ken/dev/programs/python/pims/sandbox/data/bowl.wav")
    tones = range(-25,25)
        
    # FIXME this is a kludge to make this work (to just use 1st column)
    bowl_sound = bowl_sound[:, 0]
    
    #bowl_sound, params = aiffread('/Users/ken/Sounds/tibetan.aiff')
    #fps = 44100
    
    transposed = [pitchshift(bowl_sound, n) for n in tones]   

    pygame.mixer.init(fps, -16, 1, 512) # so flexible ;)
    screen = pygame.display.set_mode((640,480)) # for the focus
    
    # Get a list of the order of the keys of the keyboard in right order.
    # ``keys`` is like ['Q','W','E','R' ...] 
    keys = open('/Users/ken/dev/programs/python/pims/sandbox/data/typewriter.kb.txt').read().split('\n')
    
    sounds = map(pygame.sndarray.make_sound, transposed)
    key_sound = dict( zip(keys, sounds) )
    is_playing = {k: False for k in keys}
    
    while True:
    
        event =  pygame.event.wait()
    
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
    
        if event.type == pygame.KEYDOWN:
    
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=50)
                is_playing[key] = True
                
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
    
        elif event.type == pygame.KEYUP and key in key_sound.keys():
    
            key_sound[key].fadeout(50) # stops with 50ms fadeout
            is_playing[key] = False

if __name__ == '__main__':
    main()  