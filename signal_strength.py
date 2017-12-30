#!/usr/bin/python
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:
from neopixel import *
import alsaaudio, time, audioop, sys

class StrengthController():
	def __init__(self, strip):

		self.strip = strip

		pixels = []
		pixels.append([8, 9, 10, 32, 33, 34])
		pixels.append([7, 11, 31, 35])
		pixels.append([6, 12, 30, 36])
		pixels.append([5, 13, 29, 37])
		pixels.append([4, 14, 28, 38])
		pixels.append([3, 15, 27, 39])
		pixels.append([2, 16, 26, 40])
		pixels.append([1, 17, 18, 19, 20, 21, 22, 23, 24, 25])

		self.pixels = pixels

		# Open the device in nonblocking capture mode. The last argument could
		# just as well have been zero for blocking mode. Then we could have
		# left out the sleep call in the bottom of the loop
		self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

		# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
		self.inp.setchannels(1)
		self.inp.setrate(8000)
		self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

		# The period size controls the internal number of frames per period.
		# The significance of this parameter is documented in the ALSA api.
		# For our purposes, it is suficcient to know that reads from the device
		# will return this many frames. Each frame being 2 bytes long.
		# This means that the reads below will return either 320 bytes of data
		# or 0 bytes of data. The latter is possible because we are in nonblocking
		# mode.
		self.inp.setperiodsize(160)

	def start(self):
		while True:
			# Read data from device
			l,data = self.inp.read()
			if l:
				# Return the maximum of the absolute value of all samples in a fragment.
				for i in range(106, 146):
					self.strip.setPixelColor(i, 0)


				try:
					volume = audioop.max(data, 2)
				except:
					volume = 3
				scaled = volume / 5000
				if scaled > 8:
					scaled = 8

				scaled = scaled - 1
				if scaled < 0:
					scaled = 0

				
				pix = self.pixels[scaled]
				for pixel in pix:
					index = 105 + pixel
					self.strip.setPixelColor(index, Color(100, 100, 100))
				self.strip.show()
			time.sleep(.001)
