import os
import sys
import shutil

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

fileNames = []
def loop_directory(directory: str):
	'''Loop files in the directory'''

	for filename in os.listdir(directory):
		if filename.endswith(".json"):
			fileNames.append(filename)

if __name__=='__main__':
	loop_directory('models/')

while True:
    try:
        isaW = int(input(bcolors.OKGREEN + "Please, select the weight of generalization relations,\n('integer' from 0 to 9): " + bcolors.ENDC ))# get ready to catch exceptions inside here
    except:      # <-- exception. handle it. loops because of while True
        print(bcolors.WARNING + "illegal, let's try that again" + bcolors.ENDC )
    else:                # <-- no exception. break
        break

while True:
    try:
        relW = int(input(bcolors.OKGREEN + "Please, select the weight of associations,\n('integer' from 0 to 9): " + bcolors.ENDC ))# get ready to catch exceptions inside here
    except:      # <-- exception. handle it. loops because of while True
        print(bcolors.WARNING + "illegal, let's try that again" + bcolors.ENDC )
    else:                # <-- no exception. break
        break

while True:
    try:
        partitionValue = int(input(bcolors.OKGREEN + "Enter the reference number of nodes for generating graph partitions\n(value ≥ 3 suggested): " + bcolors.ENDC ))# get ready to catch exceptions inside here
    except:      # <-- exception. handle it. loops because of while True
        print(bcolors.WARNING + "illegal, let's try that again" + bcolors.ENDC )
    else:                # <-- no exception. break
        break

while True:
    edgeTypes = input(bcolors.OKGREEN + "Please, enter the type of edges you want,\n('gen' (generalization), 'rel' (associations) or 'both'): " + bcolors.ENDC )
    if edgeTypes not in ('gen', 'rel', 'both'):
        print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
    else:
        break

while True: #plain, class, filtered
    if edgeTypes in ('gen'):
        normNodeType = input(bcolors.OKGREEN + "Please, enter the type of node labels,\n('ste' (stereotype), 'class', 'fil' (filtered)): "+ bcolors.ENDC )
        normEdgeType = 'null'   
        if normNodeType not in ('ste', 'class', 'fil'):
            print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
        else:
            break
    else:
        break

while True: #plain, class, filtered
    if edgeTypes in ('rel','both'):
        normNodeType = input(bcolors.OKGREEN + "Please, enter the type of node labels,\n('ste' (stereotype), 'class', 'fil' (filtered)): "+ bcolors.ENDC )
        if normNodeType not in ('ste', 'class', 'fil'):
            print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
        else:
            break
    else:
        break
    
while True:
    if normNodeType in ('fil'):
        print('Copy one of some of the following below:\nkind subkind phase role collective quantity relator category phaseMixin roleMixin mixin mode quality event historicalRoleMixin historicalRole situation type datatype enumeration')
        typeList = [item for item in input(bcolors.OKGREEN + "Enter the list items: "+ bcolors.ENDC ).split()] 
        if (any(item not in ('kind', 'subkind', 'phase', 'role', 'collective', 'quantity', 'relator', 'category', 'phaseMixin', 'roleMixin', 'mixin', 'mode', 'quality', 'event', 'historicalRoleMixin', 'historicalRole', 'situation', 'type', 'datatype', 'enumeration') for item in typeList)):
            print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n"+ bcolors.ENDC)
        else:
            break
    else:
        typeList = 'none'
        break

while True: #plain, rel, filtered
    if edgeTypes in ('rel','both'):
        normEdgeType = input(bcolors.OKGREEN + "Please, enter the type of edge labels,\n('ste' (stereotype), 'rel' (relation), 'fil' (filtered)): "+ bcolors.ENDC )
        if normEdgeType not in ('ste', 'rel', 'fil'):
            print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)   
        else:
            break
    else:
        break

while True:
    if normEdgeType in ('fil'):
        print('Copy one of some of the following below:\ncharacterization comparative externalDependence material mediation componentOf memberOf subCollectionOf subQuantityOf bringsAbout creation historicalDependence manifestation participation participational termination triggers instantiation')
        relList = [item for item in input(bcolors.OKGREEN + "Enter the list items: "+ bcolors.ENDC ).split()] 
        if (any(item not in ('characterization', 'comparative', 'externalDependence', 'material', 'mediation', 'componentOf', 'memberOf', 'subCollectionOf', 'subQuantityOf', 'bringsAbout', 'creation', 'historicalDependence', 'manifestation', 'participation', 'participational', 'termination', 'triggers', 'instantiation') for item in relList)):
            print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n"+ bcolors.ENDC)
        else:
            break
    else:
        relList = 'none'
        break

import time
start = time.process_time()

for i in fileNames:
    sys.argv = ['./norm.py', i, isaW, relW, partitionValue, edgeTypes, normNodeType, normEdgeType, typeList, relList]
    exec(open('./norm.py').read())

print("--- %s seconds ---" % (time.process_time() - start))

while True:
    processType = input("Continue with mining? (Y/N): " )
    if processType not in ('Y', 'N', 'n', 'y'):
        print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
    else:
        if processType in ('Y', 'y'):
            exec(open('./minersettings.py').read())
        else:
            break

sub0 = []
def loop_directory(directory: str):
	'''Loop sub-directory'''
	for folderName in os.listdir(directory):
            if folderName not in '.DS_Store':
                sub0.append('./subgraphs-single/'+folderName)

if __name__=='__main__':
	loop_directory('subgraphs-single/')
 
out = []
def loop_directory(directory: str):
	'''Loop sub-directory'''
	for folderName in os.listdir(directory):
            if folderName not in '.DS_Store':
                out.append('./output/'+folderName)

if __name__=='__main__':
	loop_directory('output/')

sub1 = []
def loop_directory(directory: str):
	'''Loop files in the directory'''

	for filename in os.listdir(directory):
		sub1.append(filename) 
			
if __name__=='__main__':
	loop_directory('./subgraphs-full/')

sub2 = []
def loop_directory(directory: str):
	'''Loop files in the directory'''

	for filename in os.listdir(directory):
		sub2.append(filename) 
			
if __name__=='__main__':
	loop_directory('./subgraphs-meta/')

sub3 = []
def loop_directory(directory: str):
	'''Loop files in the directory'''

	for filename in os.listdir(directory):
		sub3.append(filename) 
			
if __name__=='__main__':
	loop_directory('./subgraphs-source/')
   
while True:
    processType = input("Want to clear folders (Y/N): " )
    if processType not in ('Y', 'N', 'n', 'y'):
        print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
    else:
        if processType in ('Y', 'y'):
            for i in sub0:
                shutil.rmtree(i)
            for j in out:
                shutil.rmtree(j)
            for x in sub1:
                os.remove(os.path.join('./subgraphs-full/', x))  
            for x in sub2:
                os.remove(os.path.join('./subgraphs-meta/', x))  
            for x in sub3:
                os.remove(os.path.join('./subgraphs-source/', x))  
            print("BYE!")
        break
