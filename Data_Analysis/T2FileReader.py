## Companion file to T2TemperatureLogger.ino
## Writes information in .txt file to a .csv file
## Author(s): Justin Lawrence
## Last edited: 12/01/2020

import csv

## CONSTANTS, ALWAYS MAKE SURE THEY'RE SET CORRECTLY BEFORE RUNNING

TEXT_FILE_NAME = "DATA.txt" # Name of text document
CSV_FILE_NAME = "rawdata.csv" # Name of csv document
DATE = "01/01/2001" # Date of data collection in dd/mm/yyyy format
MATERIAL = "Brass" # String containing the name of the material used

csvFile = open(CSV_FILE_NAME, 'w', newline='') # Open csv file for writing
csvWriter = csv.writer(csvFile) # Open csv writer for constants
csvWriter.writerow(["Date", DATE, "Material", MATERIAL]) # Write constant to file
csvWriter = csv.DictWriter(csvFile, fieldnames=["Time(ms)","TempOne)(K)","TempTwo(K)","TempThree(K)"]) # Open csv writer proper
csvWriter.writeheader() # Self-explanatory
txtFile = open(TEXT_FILE_NAME, 'r') # Open txt file for reading

currentLine = txtFile.readline() # Read first line of txt file
currentReadings = dict() # Create dictionary for current readings

while (currentLine != ""): # == "" at end of file
    currentReadings["Time"] = int(currentLine) ## Read information
    currentReadings["TempOne"] = float(txtFile.readline()) + 273.15 # To kelvin
    currentReadings["TempTwo"] = float(txtFile.readline()) + 273.15
    currentReadings["TempThree"] = float(txtFile.readline()) + 273.15
    csvWriter.writerow(currentReadings) # Write information to new row
    currentLine = txtFile.readline()

txtFile.close() # Close files
csvFile.close()
