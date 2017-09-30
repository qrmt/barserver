from neopixel import *

class Pixel():
	def __init__(self, index=0, count=13):
		self.index = index
		self.count = count

	def lightPixel(self, strip, color):
		for i in range(self.index, self.index + self.count):
			strip.setPixelColor(i, color)

	def shutPixel(self, strip):
		for i in range(self.index, self.index + self.count):
			strip.setPixelColor(i, 0)
