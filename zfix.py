import os,sys
def startFix(file_Name):
    newLine = "		\"bhopleavespeed\"		\"290.000000\"\n"
    oldLine = "		\"bhopleavespeed\"		\"250.000000\""
    swap = []
    # reading data into te swap
    with open(file_Name,'r+') as hData:
        for line in hData:
            if oldLine in line:
                line = newLine
            swap.append(line)
    # reading swap data into the outputfile
    with open(file_Name, 'r+') as oData:
        for line in swap:
            oData.write('{}'.format(line))
    
    # fallthrough
    print("Success: {}".format(file_Name))
    
def file_Grab(directory):
    for file_ in os.listdir(directory):
        if file_.endswith(".zon"):
            print("Found file_: {}".format(file_))
            startFix(directory + '/' + file_)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Missing target directory")
    else:
        file_Grab(sys.argv[1])
