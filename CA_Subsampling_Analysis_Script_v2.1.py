#*****BeginHeader***************************************************************************************************
#
# Author: Jeff Davids
# Company: H2oTech
# Date: 160613
# Version: v2.0
# Mod1 Date: 
# Mod1 By: 
# Mod1 Comments: 
# Mod2 Date: 
# Mod2 By: 
# Mod2 Comments: 
# 
# 
# Purpose:  
# Randomly subSample an input file and save data in new output file
#
# Instructions: 
# Edit variables and run python script
# Python script can be called from Windows Task Manager, Cron, etc. 
#
#*****EndHeader***************************************************************************************************

#   Append the necessary inputFilePaths to the inputFilePathArray

#   Modify the following variables as desired

inputFilePathArray = []
inputFilePathArray.append(r"C:\ProgramData\TUDelft\USGS\Input")
outputFilePath = r"C:\ProgramData\TUDelft\USGS\Output"
numHeaders = 0
inputNumRecPerDay = 96
subSampleInterval = 96
numIterations = 50
fNameCriteria1 = ".csv"

#   Import system modules

import os
import sys
import datetime
import random

print("\nSubsampling input file(s), please wait...\n")
print("Average subSamplingInterval: " + str(subSampleInterval) + "\n")

#   Loop through the entire inputFilePathArray

for inputFilePath in inputFilePathArray:

#   Create directory list and iterate to the next fName if fNameCriteria1 and fNameCriteria2 isn't found

    dirList=os.listdir(inputFilePath)

    for fName in dirList:
        if fName.find(fNameCriteria1) > 0:
            inFile = open(inputFilePath + '/' + fName, 'r')
            print("Subsampling " + fName + "\n")
        
#   determines the total number of lines in inFile

            numLines = sum(1 for line in inFile)
            print("Input file total lines: " + str(numLines) + "\n")
            inFile.seek(0)

#   Next function makes an array of the offset in bytes that each new line in the file starts at
#   The lineOffset array can then be used to navigate to any line in the file
        
            lineOffset = []
            offset = 0
        
            for line in inFile:
                lineOffset.append(offset)
                offset += len(line) + 1
            inFile.seek(0)

#   Try opening the output file and throw error if not possible
        
            try: 
                outFile = open(outputFilePath + '/' + 'Subsampled_' + str(subSampleInterval) + "_" + str(numIterations) + "_" + fName , 'w')
            except IOError:
                print("\nOutput file Trunc_" + fName + " in " + outputFilePath + " folder can not be opened. Please check to see if the file is open in another application and try again.")
                continue
     
#   Skip headers in input file(s)
     
            i = 0
            while i < numHeaders:
                inFile.readline()
                i += 1
               
#   for numIterations randomly chose a line every subSampleInterval apart on average
            
            i = 1
            while i <= numIterations:
                print("Iteration Number: " + str(i) + "\n")
                currentLine = subSampleInterval / 2
                randomOffset = int(round(random.randint(0 , subSampleInterval) - subSampleInterval / 2,0))
                lastRandomLine = 0
                randomLine = currentLine + randomOffset
                inFile.seek(lineOffset[randomLine])
                dataRow = inFile.readline()
                dataField = dataRow.split(",")
                siteID = dataField[2]
                newSiteID = dataField[2]
                subSampleNumber = 0
                writeData = False

                while len(dataRow) > 0 and randomLine < numLines:
                

                    
#   Don't write data to the file the first time through because we need two sets of data to calculate volume
                    
                    if writeData == True:

#   volumeCM needs to be calculated once the lastRandomLine and randomLine are known which is on the second time in the while loop
                    
                        volumeCM = round(flowCMS * (86400 / inputNumRecPerDay) * (randomLine - lastRandomLine),0)
                        outFile.write("%s,%s, %s, %s,%s,%s,%s,%s\n" % (i, subSampleInterval, subSampleNumber, siteID, dateTime, flowCFS, flowCMS, volumeCM))
                    
                    inFile.seek(lineOffset[randomLine])
                    dataRow = inFile.readline()
                    dataField = dataRow.split(",")
                    newSiteID = dataField[2]

#   increment subSampleNumber by one if the newSiteID is the same as the siteID from the previous iteration
#   if not, reset the subSampleNumber to 1
                    
                    if newSiteID == siteID:
                        subSampleNumber += 1
                    else:
                        subSampleNumber = 1
                        
                    writeData = True
                    siteID = dataField[2]
                    dateTime = dataField[3]
                    flowCFS = dataField[7]
                    flowCMS = round(float(dataField[7]) * (1 / 35.3147),5)
                    currentLine = currentLine + subSampleInterval
                    randomOffset = random.randint(0 , subSampleInterval) - subSampleInterval / 2
                    lastRandomLine = randomLine
                    randomLine = currentLine + randomOffset
                    
                i += 1

#   Clean-up

            inFile.close()
            outFile.close()
            continue