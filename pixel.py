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

	def lightIndividualLed(self, strip, led_index, color):
		if led_index > self.count or led_index < 0:
			return
		globalIndex = self.index + led_index
		strip.setPixelColor(globalIndex, color)

	def shutIndividualLed(self, strip, led_index):
		if led_index > self.count or led_index < 0:
			return
		globalIndex = self.index + led_index
		strip.setPixelColor(globalIndex, 0)
