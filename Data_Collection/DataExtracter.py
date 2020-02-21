# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 22:36:33 2020

@author: justin
"""

import serial
import csv
import sys

CSV_FILE_NAME = "rawdata.csv" # Name of csv document
DATE = "24/01/2020" # Date of data collection in dd/mm/yyyy format
MATERIAL = "Aluminium" # String containing the name of the material used

temperatures = list() ## List of readings
currentReading = [0,0,0,0,0,0,0,0,0] ## Current reading
names = ["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven","Atmospheric"] # Array of names for columns
firstFifty = True # Check for 50C alert?
firstSeventyFive = True # Check for 75C alert?
firstHundred = True # Check of 100C alert?

ardPort = serial.Serial("COM3", 9600) ## Initializes serial port named com3, baud rate 9600

def terminationSequence():
    readingWrite = dict() # Dictionary for writing information to csv
    csvFile = open(CSV_FILE_NAME, 'w', newline='') # Open csv file for writing
    csvWriter = csv.writer(csvFile) # Open csv writer for constants
    csvWriter.writerow(["Date", DATE, "Material", MATERIAL]) # Write constant to file
    csvWriter = csv.DictWriter(csvFile, fieldnames=names) # Open csv writer proper
    csvWriter.writeheader() # Self-explanatory
    for i in range (len(temperatures)): # Iterate through readings
        currentReading = temperatures[i] # Get reading
        readingWrite["Time"] = currentReading[0] # Save time
        for j in range(1, len(names)): # Save temperatures
            readingWrite[names[j]] = currentReading[j] + 273.15
        csvWriter.writerow(readingWrite) # Write information to new row
    csvFile.close() # Close file, save information
    sys.exit(0) # End program

needed = 45 # Number of bytes for a valid reading
skip = False # Setup

while True:
    try:
        while (ardPort.in_waiting < needed): # Loop while not enough data is availible
            pass
        for i in range(9):
            x = ardPort.readline()#.decode().rstrip()
            print(x)
            currentReading[i] = float(x) # Get and process data from serial
            if (i == 0): # If flushcode
                if (currentReading[i] == 0):
                    print("Clearing buffer")
                    ardPort.reset_input_buffer() # Flush buffer, reset size
                    print(ardPort.in_waiting)
                    skip = True
                    needed = 0
                    break
            else: # Not the time
                if (firstFifty and currentReading[i] >= 50): # Alert for 50C
                    print(50)
                    firstFifty = False
                elif (firstSeventyFive and currentReading[i] >= 75): # Alert for 75C
                    print(75)
                    firstSeventyFive = False
                elif (firstHundred and currentReading[i] >= 100): #Alert for 100C
                    print(100)
                    firstHundred = False
        needed += 45 # Previously read bytes are no longer counted
        if (not skip):
            temperatures.append(currentReading.copy()) # Add to list of temperature reading
            continue
        skip = False
    except (serial.SerialException): ## Exception thrown if port is closed
        terminationSequence() ## If the port is closed, call termination sequence
        