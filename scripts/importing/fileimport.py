import os
import shutil

subdirectoryNames = []
def loop_directoryA(directory: str):
	'''Loop sub-directory'''
	for folderName in os.listdir(directory):
            if folderName not in ('.DS_Store', 'README.md'):
                subdirectoryNames.append('./ontouml-models-master/'+folderName)

#if __name__=='__main__':
loop_directoryA('ontouml-models-master/')
#loop_directoryA('Users/mattiafumagalli/Documents/GitHub/ontouml-models')
print(subdirectoryNames)

fileNames = []
def loop_directoryB(directory: str):
	'''Loop files in the directory'''

	for filename in os.listdir(directory):
		if filename.endswith(".json"):
			fileNames.append(filename)

#if __name__=='__main__':
for i in subdirectoryNames:
    loop_directoryB(i)
print(fileNames)

for f,d in zip(fileNames,subdirectoryNames):
    old_name = d +"/"+ f
    new_name = d +"/"+ "{}.json".format(d).replace('./ontouml-models-master/','')
    os.rename(old_name, new_name)
    
fileNamesNew = []
def loop_directoryC(directory: str):
	'''Loop files in the directory'''

	for filename in os.listdir(directory):
		if filename.endswith(".json"):
			fileNamesNew.append(filename)

#if __name__=='__main__':
for i in subdirectoryNames:
    loop_directoryC(i)
print(fileNamesNew)
    
destination_folder = './modelsoutput/'

for f,d in zip(fileNamesNew,subdirectoryNames):
    source = d +"/"+ f
    destination = destination_folder
    if os.path.isfile(source):        
        shutil.copy(source, destination)
        #print('copied', f)


