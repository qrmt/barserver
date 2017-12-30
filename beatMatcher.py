
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
        self.delay = 0.15
        self.lighted = False
        self.last_was_beat = False
        self.lastColorId = 0
        self.smoothMode = True
        self.show_amplitude_bars = True


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
        counter = 0

        avg_buffer = np.ones(self.window_length)
        # Set up audio
        data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
        data_in.setchannels(self.no_channels)
        data_in.setrate(self.sample_rate)
        data_in.setformat(aa.PCM_FORMAT_S16_LE)
        data_in.setperiodsize(self.chunk)


        while True:
            counter += 1
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
                    bass_range = xy[0]
                    amplitude = np.linalg.norm(bass_range)
                    total_amplitude = np.linalg.norm(xy)
                    baseline = np.average(avg_buffer)
                    ratio = amplitude / baseline
                    isBass = False
                    if (ratio > 2.5) and amplitude > 100:
                        isBass = True

                    avg_buffer = np.roll(avg_buffer, 1)
                    avg_buffer[0] = amplitude

                    if isBass and not self.lighted:
                        #print 'Beat' + str(beat_id)
                        # Potential overflow possibility here
                        beat_id += 1
                        isBass = False

                        if self.smoothMode:
                            color = self.wheel(beat_id % 255)
                        else:
                            color = self.randomWheel()

                        p_idx = 0
                        for pixel in self.pixels:
                            # Don't light the big bars, use them for amplitude viz
                            if p_idx == 8 or p_idx == 9 and self.show_amplitude_bars:
                                continue
                            pixel.lightPixel(self.strip, color)
                            p_idx += 1

                        self.lighted = True
                        #self.strip.show()
                        t = Timer(self.delay, self.shutLights)
                        t.start()

                    elif isBass and self.lighted:
                        self.last_was_beat = True
                    else:
                        self.last_was_beat = False

                    
                    # Set amplitude bars
                    level = int((14.0*total_amplitude) / 5000.0)
                    if level > 14:
                        level = 14
                    
                    if counter % 4 == 0:
                        counter = 0
                        color = self.wheel(beat_id % 255)
                        self.setAmplitudeBars(self.pixels[8], 13, 19, 34, 40, level, color)
                        self.setAmplitudeBars(self.pixels[9], 21, 27, 0, 7, level, color)
                    
                    self.strip.show()


                except audioop.error, e:
                    print e
                    continue

            time.sleep(0.005)
            #data_in.pause(0) # Resume capture

    def setAmplitudeBars(self, pxl, low, top, toprow_start, toprow_end, level, color):
        # Approx 12 levels
        # Bottom row:
        if level > 0:
            for idx in range(low, top+1):
                pxl.lightIndividualLed(self.strip, idx, color)

        # Side rows per level
        for j in range(0, level):
            top += 1
            low -= 1

            if low < 0:
                low = 0

            pxl.lightIndividualLed(self.strip, top, color)
            pxl.lightIndividualLed(self.strip, low, color)

        # If max level, light top row also
        if level == 14:
            for idx in range(toprow_start,toprow_end):
                pxl.lightIndividualLed(self.strip, idx, color)
        else:
            for idx in range(toprow_start-1,toprow_end+1):
                pxl.shutIndividualLed(self.strip, idx)

            # hack for the last led in the strip (looks like top row but at the end on pixel #10)
            pxl.shutIndividualLed(self.strip, pxl.count)



        # Shut down others
        for j in range(0, 13-level):
            top += 1
            low -= 1

            pxl.shutIndividualLed(self.strip, top)
            pxl.shutIndividualLed(self.strip, low)




    def shutLights(self):
        p_idx = 0
        for pixel in self.pixels:
            if (p_idx == 8 or p_idx == 9) and self.show_amplitude_bars:
                break
            
            pixel.shutPixel(self.strip)
            p_idx += 1

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

    def randomWheel(self):
        # Calculate new mean opposite on then circle
        mu = self.lastColorId + 127 % 255
        mu = float(mu) / 255.0
        mu = mu * 2*np.pi - np.pi

        newId = np.random.vonmises(mu, 1)
        newId = int(np.floor((newId + np.pi) / (2*np.pi) * 255.0))

        self.lastColorId = newId
        return self.wheel(newId)
