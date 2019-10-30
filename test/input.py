#!/usr/bin/env python

## recordtest.py
##
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm device for sound capture, sets
## various attributes of the capture, and reads in a loop,
## writing the data to standard out.
##
## To test it out do the following:
## python recordtest.py out.raw # talk to the microphone
## aplay -r 8000 -f S16_LE -c 1 out.raw

from __future__ import print_function

import sys
import time
import getopt
import alsaaudio
import os
home = os.environ['HOME']
sys.path.append("sibcommon")
import asoundConfig


if __name__ == '__main__':
    file_name = os.path.join(os.path.dirname(__file__), 'resources', 'audio.raw')
    print ("file_name",file_name)
    f = open(file_name, 'wb')
    hw = asoundConfig.getHw()
    # Open the device in nonblocking capture mode. The last argument could
    # just as well have been zero for blocking mode. Then we could have
    # left out the sleep call in the bottom of the loop
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, cardindex=int(hw['Mic']))

    # Set attributes: Mono, 44100 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    # For our purposes, it is suficcient to know that reads from the device
    # will return this many frames. Each frame being 2 bytes long.
    # This means that the reads below will return either 320 bytes of data
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # mode.
    inp.setperiodsize(160)
    
    loops = 5000
    while loops > 0:
        loops -= 1
        # Read data from device
        l, data = inp.read()
      
        if l:
            f.write(data)
            time.sleep(.001)
