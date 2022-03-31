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

while True:
    enter = input(bcolors.OKGREEN +"Welcome to our pattern discovery application!\nPress Enter to continue..." + bcolors.ENDC)
    if enter not in '':
        print(bcolors.WARNING + "\nWarning: Not an appropriate choice\n" + bcolors.ENDC)
    else:
        exec(open('./normsettings.py').read())
        break