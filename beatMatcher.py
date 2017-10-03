
# Python 2.7 code to analyze sound and interface with Arduino

import numpy as np   # from http://numpy.scipy.org/
import audioop
import sys
import math
import struct
from struct import unpack
import alsaaudio as aa
import time
import random
from programcontroller import Color
from pixel import *
from threading import Timer


'''
Sources
http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2
'''

class BeatMatcher():

    def __init__(self, strip, pixels):
        self.strip = strip
        self.pixels = pixels
        self.MAX = 0
        self.sample_rate = 44100
        self.no_channels = 1
        self.chunk = 512 # Use a multiple of 8

        self.window_length = 4
        self.delay = 0.1
        self.lighted = False



    def fft(self, data, log_scale=False, div_by=100):
        left, right = np.split(np.abs(np.fft.fft(data)), 2)
        ys = np.add(left, right[::-1])
        if log_scale:
            ys = np.multiply(20, np.log10(ys))
        if div_by:
            ys = ys / float(div_by)
        return ys


    def list_devices(self):
        # List all audio input devices
        print aa.pcms()


    def beatmatch(self):
        beat_id = 0

        avg_buffer = np.ones(self.window_length)
        # Set up audio
        data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
        data_in.setchannels(self.no_channels)
        data_in.setrate(self.sample_rate)
        data_in.setformat(aa.PCM_FORMAT_S16_LE)
        data_in.setperiodsize(self.chunk)


        while True:
            l,data = data_in.read()
            #data_in.pause(1) # Pause capture whilst RPi processes data
            if l:
              # catch frame error
                try:
                    npdata = np.fromstring(data,dtype='<i2')
                    xy = self.fft(npdata)

                except:
                    pass
                try:
                    bass_range = xy[0:1]
                    amplitude = np.linalg.norm(bass_range)
                    baseline = np.average(avg_buffer)
                    ratio = amplitude / baseline

                    if (ratio > 2):
                        isBass = True

                    avg_buffer = np.roll(avg_buffer, 1)
                    avg_buffer[0] = amplitude

                    if isBass and not self.lighted:
                        #print 'Beat' + str(beat_id)
                        beat_id += 1
                        isBass = False

                        color = self.wheel(beat_id % 255)
                        for pixel in self.pixels:
                            pixel.lightPixel(self.strip, color)

                        self.lighted = True
                        self.strip.show()
                        t = Timer(self.delay, self.shutLights)
                        t.start()


                except audioop.error, e:
                    print e
                    continue

            time.sleep(0.005)
            #data_in.pause(0) # Resume capture


    def shutLights(self):
        for pixel in self.pixels:
            pixel.shutPixel(self.strip)

        self.strip.show()
        self.lighted = False

    def wheel(self, pos):
    	if pos < 85:
    		return Color(pos * 3, 255 - pos * 3, 0)
    	elif pos < 170:
    		pos -= 85
    		return Color(255 - pos * 3, 0, pos * 3)
    	else:
    		pos -= 170
    		return Color(0, pos * 3, 255 - pos * 3)
