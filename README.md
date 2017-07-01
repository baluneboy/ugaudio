# ugaudio
A somewhat magnificent application for converting acceleration data to audio files.

**IMPORTANT**

***Before*** attempting to listen to any of the sound files that this program
produces, adjust your system volume to a safe level.  The ugaudio software does
not guarantee that the sound produced will be either pleasant or at a desirable
volume.

**DEPENDENCIES**: python, numpy, scipy, matplotlib, and pygame

*NICE TO HAVE*:
: sox (the Swiss Army knife of sound processing programs)
: audacity (sound editing program)

**PRACTICAL CONSIDERATIONS**

There are important considerations and tradeoffs that come with converting
acceleration data into sound that is audible to humans. Perhaps the most
important consideration is the ***human hearing*** system and its ***limitations***.

Wikipedia suggests that humans can hear sound in the frequency range (pass-band)
from about 20 Hz to 20 kHz. Some humans likely have a narrower or truncated
pass-band. A typical Space Acceleration Measurement System (**SAMS**) data file is
sampled at 500 sa/sec with a pass-band from about 0.01 Hz to about 200 Hz, **so
there is a relatively small amount of overlap between SAMS pass-band and human
hearing pass-band**. If you're a purist, then you'd leave the "-r" switch off of
the command line and attempt to listen and probably miss some interesting
features in the ug environment below 20 Hz. If you want to explore, then adjust
frequencies by using the "-r" switch **BUT** keep in mind that what you hear has
been distorted in time/frequency to enable you to hear more of the measurement
information...this is kinda like using an infrared camera for seeing otherwise
invisible portions of the electromagnetic (light) spectrum.

Another consideration is how to 3 map spatial coordinates from acceleration
measurements to typically 2 channels of audio. One method is to use the x-axis
as left channel and y-axis for right channel of a stereo track, but what about
the z-axis? This deserves more thought and attention, but here (for now) we just
happily ignore the issue. The "s" output is a "cocktail party" approach, with each
of the x-, y-, and z-axis as different "conversations" all superimposed.

<< FIXME with better versions of the following and with better explanations too
MAYBE MORE/BETTER HOME BREWED SAMPLES >>

See the test files (written like accel. data, PAD) in the examples folder, and note
the following:

for test1.pad, the x-axis is 40 Hz sinusoid, y is 80 kHz, and z is 5 kHz with sample
rate of 44100 sa/sec; so

- if you run "`convert.py -a 4 test1.pad`"
then listen, you should **not** likely hear the x-axis sound file

- if you run "`convert.py -a 4 -r 11025 test1.pad`"
then listen, you should **only hear** the z-axis and s-axis sound file

<< test2.pad - FIXME >>


# BLOOPERS
 
Aa quick acknowledgement to my neighbors who may have heard more than a
few strange sounds coming from my general direction during development.

**Wanna hear a bird chirping on the International Space Station!?**

1. Download/convert the following file:

convert.py -r 22050 2014_10_17_06_31_15.515+2014_10_17_06_41_15.528.121f02

*okay, it was not really a bird...the "-r" switch resampled to higher pitch*

2. Listen to "bird" excerpt of this recording using sox's play command:

play 2014_10_17_06_31_15.515+2014_10_17_06_41_15.528.121f02s.aiff trim 9 5

or this command to apply band-pass filter (center = 2500 Hz, width = 500 Hz)

play 2014_10_17_06_31_15.515+2014_10_17_06_41_15.528.121f02s.aiff trim 9 5 2.5k 500h

3. Alternatively, open resulting AIFF file with Audacity:

open -a Audacity 2014_10_17_06_31_15.515+2014_10_17_06_41_15.528.121f02s.aiff

3. Use the I-beam tool in Audacity to select the portion of the signal between
about the 9-sec and 14-sec mark, then give that a listen.
