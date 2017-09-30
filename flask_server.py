from flask import Flask
from flask import render_template
from flask import request

from controller import Controller
import time


app = Flask(__name__)

abort_current = 0
controller = Controller()

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/worm')
def worm():
	global controller

	controller.runWormChase()

	return 'Success'

@app.route('/checker')
def checker():
	global controller
	controller.runCheckerPattern()

	return 'Success'

@app.route('/random')
def randomPattern():
	global controller
	controller.runRandomColor()
	return 'Success'

@app.route('/stop')
def stopLights():
	global controller
	controller.stopLights()
	return 'Success'

@app.route('/panic')
def panicMode():
	global controller
	controller.runPanicMode()
	return 'Success'

@app.route('/rainbow')
def rainbow():
	global controller
	controller.runRainbow()
	return 'Success'

@app.route('/fft')
def fft():
	global controller
	controller.fftRunner()
	return 'Success'


@app.route('/rainbowCycle')
def rainbowCycle():
	global controller
	controller.runRainbowCycle()
	return 'Success'

@app.route('/setColor', methods=['POST'])
def setColor():
	data = request.json

	red = data['r']
	green = data['g']
	blue = data['b']

	global controller
	controller.setFullColor(red, green, blue)
	return 'Success'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', threaded=False)
