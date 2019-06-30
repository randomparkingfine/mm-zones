# Changes start zone speed to a standard 290 u/s instead of 250 u/s
# NOTE: This script best used for patches below 0.8 
import os,sys
def start_Fix(file_Name):
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

def to_Fix(target):
    oldLine = "		\"bhopleavespeed\"		\"250.000000\""
    with open(target, 'r') as tData:
        for line in tData:
            if oldLine in line:
                return True
    return False

def file_Grab(directory):
    for file_ in os.listdir(directory):
        if file_.endswith(".zon") and to_Fix(directory + '/' + file_):
            print("Found file_: {}".format(file_))
            start_Fix(directory + '/' + file_)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Missing target directory")
    else:
        file_Grab(sys.argv[1])
