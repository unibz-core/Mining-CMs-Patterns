import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

folderNames = []
def loop_directory(directory: str):
	'''Loop sub-directory'''
	for folderName in os.listdir(directory):
            if folderName not in '.DS_Store':
                folderNames.append('/subgraphs-single/'+folderName)
			
if __name__=='__main__':
	loop_directory('subgraphs-single/')

while True:
    MiningType = input(bcolors.OKGREEN + "'single', 'full' or meta?: " + bcolors.ENDC)
    if MiningType not in ('single', 'full', 'meta'):
        print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
    else:
        break

while True: 
    try:   
        MaxpatternsNo = int(input(bcolors.OKGREEN + "MaxpatternsNo (eg. 50): " + bcolors.ENDC ))# get ready to catch exceptions inside here
    except:      # <-- exception. handle it. loops because of while True
        print(bcolors.WARNING + "illegal, let's try that again" + bcolors.ENDC )
    else:                # <-- no exception. break
        break

while True: 
    try:   
        MinpatternsLen = int(input(bcolors.OKGREEN + "MinpatternsLen (eg. 2): " + bcolors.ENDC ))# get ready to catch exceptions inside here
    except:      # <-- exception. handle it. loops because of while True
        print(bcolors.WARNING + "illegal, let's try that again" + bcolors.ENDC )
    else:                # <-- no exception. break
        break

while True: 
    try:   
        MinpatternsFreq = int(input(bcolors.OKGREEN + "MinpatternsFreq (eg. 2): " + bcolors.ENDC ))# get ready to catch exceptions inside here
    except:      # <-- exception. handle it. loops because of while True
        print(bcolors.WARNING + "illegal, let's try that again" + bcolors.ENDC )
    else:                # <-- no exception. break
        break

singleFolder = '/subgraphs-full'
metaFolder = '/subgraphs-meta'

def minType(x):
    if 'single' in x:
        return folderNames
    if 'full' in x: 
        return singleFolder
    if 'meta' in x: 
        return metaFolder

path = minType(MiningType)

import time
start = time.process_time()

import sys
if type(path) == str:
    sys.argv = ['./miner.py', path, MaxpatternsNo, MinpatternsLen, MinpatternsFreq]
    exec(open('./miner.py').read())
else:
    for i in path:
        sys.argv = ['./miner.py', i, MaxpatternsNo, MinpatternsLen, MinpatternsFreq]
        exec(open('./miner.py').read())

print("--- %s seconds ---" % (time.process_time() - start))