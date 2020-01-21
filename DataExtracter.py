# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 22:36:33 2020

@author: justin
"""

import serial
import csv
import sys

CSV_FILE_NAME = "rawdata.csv" # Name of csv document
DATE = "01/01/2001" # Date of data collection in dd/mm/yyyy format
MATERIAL = "Brass" # String containing the name of the material used

temperatures = list() ## List of readings
currentReading = [0,0,0,0,0,0,0,0,0] ## Current reading
names = ["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven","Atmospheric"] # Array of names for columns

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

while True:
    try:
        while (ardPort.in_waiting < needed): # Loop while not enough data is availible
            pass
        for i in range(9):
            currentReading[i] = float(ardPort.readline().decode().rstrip()) # Get and process data from serial
        needed += 45 # Previously read bytes are no longer counted
        temperatures.append(currentReading.copy()) # Add to list of temperature readings
        
    except (serial.SerialException): ## Exception thrown if port is closed
        terminationSequence() ## If the port is closed, call termination sequence
        