# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 21:49:30 2020

@author: justi
"""

import csv

# Data in both files should be normalized to start at T = 0s, and run at the same intervals for the same amount of time
CSV_DATA_FILE_NAME = "processed_data.csv" # Name of csv document with processed data
CSV_MODEL_FILE_NAME = "model_data.csv" # Name of the csv document with model data
names = ["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven","Atmospheric"] # Array of names for columns



def calculateMean(): # Calculates the mean of the data
    total = [0,0,0,0,0,0,0] # Sum of all data points
    num = [0,0,0,0,0,0,0] # Number of data points
    csvFile = open(CSV_DATA_FILE_NAME, 'r', newline='') # Open csv file for reading
    csvReader = csv.DictReader(csvFile, fieldnames = names) # Open proper reader
    skip = 0 # Counter to skip first two rows
    for row in csvReader: # Iterate through rows
        if skip >= 2: # Get past first two rows
            for i in range (1,7): # Iterate through names of temperatures
                total[i-1] += float(row[names[i]]) # Add each temperature to total
                num[i-1] += 1 # Update number of readings
        skip += 1
    csvFile.close() # Close file
    means = list() # Mean values
    for i in range(0,7): # Iterate through each array
        means.append(total[i]/num[i]) # Calculate and add mean
    return means

def calcSumSquares():
    means = calculateMean() # Get the means
    total = [0,0,0,0,0,0,0] # Sum of all variances
    csvFile = open(CSV_DATA_FILE_NAME, 'r', newline='') # Open csv file for reading
    csvReader = csv.DictReader(csvFile, fieldnames = names) # Open proper reader
    skip = 0 # Counter to skip first two rows
    for row in csvReader: # Iterate through rows
        if skip >= 2: # Get past first two rows
            for i in range (1,7): # Iterate through names of temperatures
                num = float(row[names[i]]) # Get value
                variance = (num - means[i-1])**2 # Calculate variance
                total[i-1] += variance # Add to total variances
        skip += 1
    csvFile.close() # Close file
    means = list() # Mean values
    return total

def calcSumResiduals():
    total = [0,0,0,0,0,0,0] # Sum of all residuals squared
    csvDataFile = open(CSV_DATA_FILE_NAME, 'r', newline='') # Open csv files for reading
    csvModelFile = open(CSV_MODEL_FILE_NAME, 'r', newline='')
    csvDataReader = csv.DictReader(csvDataFile, fieldnames = names) # Open proper readers
    csvModelReader = csv.DictReader(csvModelFile, fieldnames = names) # Open proper readers
    skip = 0 # Counter to skip first two rows
    for i in range(0, len(csvDataReader)): # Iterate through rows
        if skip >= 2: # Get past first two rows
            for j in range (1,7): # Iterate through names of temperatures
                data = float(csvDataReader[i][names[j]]) # Get data value
                model = float(csvModelReader[i][names[j]]) # Get model value
                residual = (data - model)**2 # Square of residual
                total[j-1] += residual # Add to total residuals
        skip += 1
    csvDataFile.close() # Close files
    csvModelFile.close()
    return total    

def calculateRScore():
    sumSquares = calcSumSquares()
    sumResiduals = calcSumResiduals()
    RScores = list() # List of r^2-scores
    for i in range(0,7): # Iterate through locations
        RScores.append(1-sumResiduals[i]/sumSquares[i]) # Calculate and add r^2 scores
    return RScores

scores = calculateRScore()
print(scores)
        