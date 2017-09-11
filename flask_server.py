from flask import Flask
from controller import Controller
import multiprocessing
import time


app = Flask(__name__)

abort_current = 0
controller = Controller()
current_process = None


@app.route('/worm')
def worm():
	global current_process

	if current_process:
		current_process.terminate()
	current_process = multiprocessing.Process(target=controller.runWormChase)
	current_process.start()

	return 'LOL'

@app.route('/checker')
def checker():
	global current_process
	if current_process:
		current_process.terminate()
	current_process = multiprocessing.Process(target=controller.runCheckerPattern)
	current_process.start()

	return 'LOL'

@app.route('/random')
def randomPattern():
	global current_process
	if current_process:
		current_process.terminate()
	current_process = multiprocessing.Process(target=controller.runRandomColor)
	current_process.start()
	return 'LOL'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
