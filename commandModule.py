import random
import os
import json

loadedInputs = {}


##
#   Choose a command from the command options
##
def getCommand(inputSheetList) :
	global loadedInputs

	randInputListNumber = random.randint(0, len(inputSheetList) - 1)
	randInputList = inputSheetList[randInputListNumber]
	randInputNumber = random.randint(0, len(loadedInputs[randInputList]) - 1)

	return loadedInputs[randInputList][randInputNumber]



def loadInputsFromFile(btnDir, filename) :
	global loadedInputs

	file = open(btnDir + '/' + filename,'r')
	loadedInputs[filename[:-5]] = []
	for line in file :
		j = json.loads(line)
		loadedInputs[filename[:-5]].append(j)


def generateCmdRequest(cmd) :
	#print (cmd)
	if (cmd['type'] != 'BUTTON') :
		r = random.randint(0, len(cmd['values']) - 1)
		cmdStr = cmd['cmdText'] + str(cmd['values'][r])
		inputReq = cmd['values'][r]
	else :
		cmdStr = cmd['cmdText']
		inputReq = cmd['inputId']


	retval = {
		'commandString': cmdStr,
		'inputReq': inputReq
	}

	return retval




for filename in os.listdir('inputs'):
     loadInputsFromFile('inputs', filename)


#print (loadedInputs);