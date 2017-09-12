from flask import Flask
from controller import Controller
import time


app = Flask(__name__)

abort_current = 0
controller = Controller()


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

@app.route('/rainbow')
def rainbow():
	global controller
	controller.runRainbow()
	return 'Success'


@app.route('/rainbowCycle')
def rainbowCycle():
	global controller
	controller.runRainbowCycle()
	return 'Success'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
