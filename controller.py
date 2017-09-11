from programcontroller import *
from pixel import Pixel
import time
import random
from signal_strength import StrengthController
from multiprocessing import Process
from functools import wraps
import sys

# LED strip configuration:
LED_COUNT      = 155      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 120# 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PIXEL_AMOUNT   = 12




class Controller():
	def __init__(self):

		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
		self.strip.begin()

		self.program = Program(self.strip, PIXEL_AMOUNT)
		self.currentProcess = None

		'''Create pixels'''
		self.pixels = []
		ind = 0
		for p in range(0, PIXEL_AMOUNT):
			if p == 2:
				amount = 14
			else:
				amount = 13
			pixel = Pixel(ind, amount)
			ind = ind + amount

			self.pixels.append(pixel)

		# Strength
#		strength = StrengthController(self.strip)
#		sproc = multiprocessing.Process(target=strength.start)
#		sproc.start()

	def terminate(func):
		@wraps(func)
		def terminateCurrentProcess(self, *args, **kwargs):
			if self.currentProcess:
				if self.currentProcess.is_alive():
					self.currentProcess.terminate()

			return func(self, *args, **kwargs)
		return terminateCurrentProcess

	@terminate
	def runWormChase(self):
		def chase():
			while (True):
				color = randomColor()

				wormPixels = []
				i = 0
				while i < len(wormPixels):
					wormPixels.append(self.pixels[i])
					i = i + 2

				i = 1
				while i < len(wormPixels):
					wormPixels.append(self.pixels[i])
					i = i + 2

				self.program.wormChase(color, 1000, 2, wormPixels)

		self.currentProcess = Process(target=chase)
		self.currentProcess.start()

	@terminate
	def runCheckerPattern(self):
		def checker():
			while(True):
				color = randomColor()
				self.program.checkerPattern(color, 300, self.pixels)

		self.currentProcess = Process(target=checker)
		self.currentProcess.start()

	@terminate
	def runRandomColor(self):
		def randomColor():
			self.program.randomColor(self.pixels)

		self.currentProcess = Process(target=randomColor)
		self.currentProcess.start()

	@terminate
	def setFullColor(self, color):
		self.program.setFullColor(self.pixels, color)

	@terminate
	def runPanicMode(self):
		def panicMode():
			while(True):
				self.program.setFullColor(self.pixels, Color(255,0,0))
				time.sleep(0.5)
				self.program.shutPixels(self.pixels)
				time.sleep(0.5)

		self.currentProcess = Process(target=panicMode)
		self.currentProcess.start()


	@terminate
	def stopLights(self):
		self.program.shutPixels(self.pixels)

def randomColor():
	blue = random.randint(0,255)
	red = random.randint(0,255)
	green = random.randint(0,255)
	return Color(red, green, blue)

#controller = Controller()
#controller.runCheckerPattern()
#controller.runRandomColor()
#controller.setFullColor(Color(255,0,80))
#controller.runPanicMode()
#controller.runWormChase()
#controller.colorChooser()
