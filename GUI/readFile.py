from calc import calcFlowRate
import csv
def checkFile(fName):
    file = open(fName, 'r')
    lines = file.readlines()
    count = 0

    # check the file for errors 
    for line in lines:
        count += 1
        # check if line includes a comma

        # split the line at the comma
        inp = line.split(',')

        # get the shear stress value
        stress = float(inp[0].strip())

        # check if the shear stress value is in range

        # get the time values
        time = inp[1].strip()

        # split the time variables by the colons
        time = time.split(":")

        # check if correct number of colons present
        if len(time) != 3:
            # error in time input of file
            print("Error in file input: time input is incorrect on line [{}]. Correct format[ hrs:mins:sec ]".format(count))
            break

        print("{}: {} , {}".format(count, stress, time))
    
    
#flow = calcFlowRate(float(stress))
#rint(flow)


