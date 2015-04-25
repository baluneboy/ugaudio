~/sox/play fiona.aiff gain -12 phaser 0.6 0.66 4 0.6 2 -t reverb stretch 3

# Try the following to do some low-level testing on this package.

# Change to ugaudio directory, then use the following command for non-verbose testing...
# you should get "OK" in bottom line if all went okay.
python -m unittest discover -s tests -p 'test_*.py'

# Change to ugaudio directory, then use the following command for verbose testing...
# you should get "OK" in bottom line if all went okay.
python -m unittest discover -s tests -p 'test_*.py' -v

# Some other, higher-level testing that you might consider:
# ------------------------------------------------------------------------------
# Scenario #1: given a linear chirp with amplitude and frequency ranges that are
#              representative of the loudest ISS vibratory microgravity
#              environment, we should expect a portion of that signal (below 20
#              Hz and perhaps even higher than that) to be inaudible
#
# 1. Create linear chirp signal (described above) and save as acceleration file:
command goes here

# 2. Convert the acceleration file to audio AIFF file:
command goes here

# 3. Listen to the audio AIFF file and try to gauge at what time during playback
#    you start to hear the signal:
command goes here

# 4. Multiply the time you first hear sound in seconds relative to the start of
#    playback and multiply that by WHAT SCALE FACTOR to get approximate lower
#    end of your hearing frequency range:
command goes here

# ------------------------------------------------------------------------------
# Scenario #2: given the same scenario as Test Case #1, except that we convert
#              using a new, higher rate we now expect to hear more (longer
#              duration) of the chirp
#
# 1. Do steps #1 and #2 shown in Scenario #1 above.

# 2. Convert acceleration to audio AIFF file, but use a new, higher rate:
command goes here

# 3. Listen to the audio and notice this is a technique you can use to hear
#    the otherwise inaudible, kinda like night-vision goggles.  Of course,
#    in this scenario, we are intentionally distorting the signal.
