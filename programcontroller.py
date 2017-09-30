from pixel import *
import random
import time
from beatMatcher import BeatMatcher


def Color(red, green, blue):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (red << 16) | (green << 8) | blue


class Program():
	def __init__(self, strip, matrix_size):
		self.strip = strip
		self.matrix_size = matrix_size

	def beatMatching(self, pixels):
		matcher = BeatMatcher(self.strip, pixels)
		matcher.beatmatch()


	def wormChase(self, color, wait_ms, worm_size, pixels):
		'''worm that goes around'''
		for i in range(0, len(pixels)):
			for pixel in pixels:
				pixel.shutPixel(self.strip)

			pixels_to_light = []
			for p in range(0, worm_size):
				pixels_to_light.append((i + p) % self.matrix_size)

			for pixel in pixels_to_light:
				pixel.lightPixel(self.strip, color)

			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def checkerPattern(self, color, wait_ms, pixels):
		'''checker pattern, every 2 is lighted at a time'''
		for pixel in pixels:
			pixel.shutPixel(self.strip)

		i = 0
		while i < len(pixels):
			pixels[i].lightPixel(self.strip, color)
			i = i + 2
		self.strip.show()
		time.sleep(wait_ms/1000.0)

		for pixel in pixels:
			pixel.shutPixel(self.strip)

		i = 1
		while i < len(pixels):
			pixels[i].lightPixel(self.strip, color)
			i = i + 2
		self.strip.show()

		time.sleep(wait_ms/1000.0)


	def randomColor(self, pixels):
		while(True):
			for pixel in pixels:
				blue = random.randint(0,255)
				red = random.randint(0,255)
				green = random.randint(0,255)

				color = Color(red, green, blue)

				pixel.lightPixel(self.strip, color)

			self.strip.show()
			time.sleep(0.5)


	def setFullColor(self, pixels, color):
		for pixel in pixels:
			pixel.lightPixel(self.strip, color)

		self.strip.show()

	def shutPixels(self, pixels):
		for pixel in pixels:
			pixel.shutPixel(self.strip)

		self.strip.show()

	# -------------------------------------------------------
	# Individual led functions:
	def colorWipe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(wait_ms/1000.0)


	def theaterChase(self, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, color)
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.wheel((i+j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def rainbowCycle(self, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256*iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.wheel(((i * 256 / self.strip.numPixels()) + j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChaseRainbow(self, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)
