import random
import sys, termios, tty, os, time
from threading import Timer
from threading import Thread

import commandModule

levelScore = 0
currentLevel = 0
gameActive = True;

gameSettings = {
	'levelStart': 0,
	'baseRoundTimer': 10.1,
	'roundTimerMod': .1,
	'loseCount': -10,
	'baseWinCount': 10,
	'winCountMod': 1,
	'commandSheets': ['gp1a', 'gp2a']
}


def main() :
	global gameActive
	while gameActive :
		runCommandRound()
		checkScore()
		print()


##
#   Run a Single round of the commands
##
def runCommandRound() :
	global timerThread
	global gameSettings
	global currentLevel
	global commandModule

	command = commandModule.getCommand(gameSettings['commandSheets'])
	cmdReq = commandModule.generateCmdRequest(command)

	timeout = gameSettings['baseRoundTimer'] - (gameSettings['roundTimerMod'] * currentLevel)

	timerThread = Timer(timeout, timeRanOut)
	userInputThread = Thread(target=getUserInput, args=[cmdReq['inputReq']])
	
	print (cmdReq['commandString'])

	userInputThread.start()
	timerThread.start()

	userInputThread.join(timeout)



##
#   Get the user input
##
def getUserInput(inputReq) :
	global levelScore
	global timerThread

	char = getch()

	if (char == inputReq) :
		print ('Command Correct!')
		levelScore += 1
	else : 
		print ('Command Incorrect!')
		levelScore -= 1
	timerThread.cancel()
	sys.exit(0)


##
#   Get the key a user presses
#	Note: this will change with pi
##
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
 
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch
		

##
#   Thread function for timer
##
def timeRanOut():
	global userInputThread
	global levelScore
	print ('ERROR: no command entered')
	sys.stdout.flush()
	levelScore -= 1

timerThread = Timer(0, timeRanOut)


##
#   Check win/loss
##
def checkScore() :
	global levelScore
	global currentLevel
	global gameSettings
	global gameActive
	if levelScore < gameSettings['loseCount'] - 1 :
		print()
		print ('************************')
		print ('Your ship has crashed!')
		print ('YOU LOSE')
		print ('************************')
		print()
		gameActive = False
		sys.exit(0)
	elif levelScore > (gameSettings['baseWinCount'] + (currentLevel * gameSettings['winCountMod'])) :
		currentLevel += 1
		levelScore = 0
		print()
		print ('************************')
		print ('Great job, you made it to the next quadrant!')
		print ('Entering Quadrant ' + str(currentLevel))
		print ('************************')
		print()
	
	sys.stdout.flush()




main()



