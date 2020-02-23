# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:19:51 2020

@author: justi
"""

## This program takes processed data and model data, and creates seven linear functions in excel
## one for each temperature, and calculates the R^2 value of each fit.

import csv
import xlsxwriter
from math import log as ln

# Data in both files should be normalized to start at T = 0s, and run at the same intervals for the same amount of time
CSV_DATA_FILE_NAME = "processed_data.csv" # Name of csv document with processed data
CSV_MODEL_FILE_NAME = "model_data.csv" # Name of the csv document with model data
XLSX_SHEETS_FILE_NAME = "linear_fit.xlsx" # Name of the xlsx document with the linear fit data
names = ["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven"] # Array of names for columns
header = ["Time", "DataTemperature", "ModelTemperature", "ln(Data)", "ln(Model)"]

def extractData(): # Pulls data from the csv files and stores them in lists
    data_file = open(CSV_DATA_FILE_NAME, 'r', newline='') # Open data file for reading
    data_reader = csv.DictReader(data_file, fieldnames=names) # Open data file reader
    measured_data = list() # List to hold experimental data
    skip = 0 # To skip first two rows
    for row in data_reader:
        if skip < 2: # Skip the first two rows
            skip += 1
            continue
        measured_data.append(row) # Otherwise, add the data to the list
    data_file.close() # Close file
    ## Same process, but with model data
    data_file = open(CSV_MODEL_FILE_NAME, 'r', newline='')
    data_reader = csv.DictReader(data_file, fieldnames=names)
    model_data = list()
    skip = 0
    for row in data_reader:
        if skip < 2:
            skip += 1
            continue
        model_data.append(row)
    data_file.close()
    return measured_data, model_data # Return the data lists

def getTime(measured_data): # Stores the time data in extractData as its own list
    ## This function just extists so that I only have to deal with time once
    times = list() # Create list
    for reading in measured_data: # Loops through the readings
        times.append(float(reading["Time"])) # Get time and add it to the list
    return times # Return the list of times

def processData(measured_data, model_data): # Processes the extracted data to be ready for writing for a given temperature
    ## This returns a 3d list. d1 = temperature number, d2 = data/model/ln(data)/ln(model), d3 = datapoint
    ## First, build the list
    processed_data = list() # The 3d list
    for i in range (0,7): # Append the seven tempreature lists
        processed_data.append(list())
        for k in range(0,4): # Append the four data columns to the temperature list
            processed_data[i].append(list())
            
    ## Then, input the data
    for index in range(0, len(measured_data)): # Iterates through every row of the data
        for i in range(0,7): # Iterate through temperatures
            ## Get model and experimental data
            measured = float(measured_data[index][names[i+1]])
            model = float(model_data[index][names[i+1]])
            processed_data[i][0].append(measured) # Stores the data
            processed_data[i][1].append(model)
            processed_data[i][2].append(ln(measured))
            processed_data[i][3].append(ln(model))
            
    return processed_data

def setupSheets(): # Sets up the xlsx file
    xlsx_file = xlsxwriter.Workbook(XLSX_SHEETS_FILE_NAME) # Create file
    worksheets = list() # List of xlsx_file worksheets
    for i in range(1,8): # Loop to initialize the seven sheets, one for each temperature
        worksheets.append(xlsx_file.add_worksheet("Temperature " + str(i))) # Add worksheet with proper name
    for i in range(0,7): # Loop through sheets and add headers
        worksheets[i].write_row(0,0,header) # Write the header to the sheet
    return xlsx_file, worksheets

def fillSheets(): # Fills the xlsx file with the data
    measured_data, model_data = extractData() # Get all necessary data and file handles
    times = getTime(measured_data)
    processed_data = processData(measured_data, model_data)
    xlsx_file, worksheets = setupSheets()
    for i in range(0,7): # Index for temperatures
        worksheet = worksheets[i] # Get current worksheet
        dataset = processed_data[i] # Get current node's data
        worksheet.write_column(1,0,times) # Write times to column 0, starting at row 1
        for k in range(0,4): # Iterate through data types in dataset
            worksheet.write_column(1,k+1,dataset[k]) # Write data
    xlsx_file.close() # For now, to save
    return

fillSheets()